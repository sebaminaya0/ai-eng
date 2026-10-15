"""The M3 RAG app as a production-shaped HTTP API. Built in 13.03, reused by the UIs (13.04) and the deploy (13.05).

    uv run uvicorn app:app --port 8000          # from this folder
    curl -H "Authorization: Bearer dev-key" -d '{"question": "Who was Abraham Lincoln?"}' localhost:8000/v1/ask

Config (env): APP_API_KEYS (comma-separated, default "dev-key"), APP_PROVIDER (aieng.llm provider), APP_RATE_PER_MIN (default 20).
"""
import asyncio
import json
import os
import time
from collections import defaultdict
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from aieng import rag
from aieng.llm import client

API_KEYS = set(os.getenv("APP_API_KEYS", "dev-key").split(","))
RATE_PER_MIN = int(os.getenv("APP_RATE_PER_MIN", "20"))
LLM_TIMEOUT = 30

_sync, MODEL = client(os.getenv("APP_PROVIDER"))
llm = AsyncOpenAI(base_url=str(_sync.base_url), api_key=_sync.api_key, timeout=LLM_TIMEOUT, max_retries=1)
EXTRA = {"reasoning_effort": "none"} if _sync.base_url.host == "localhost" else {}


@asynccontextmanager
async def lifespan(app):
    await asyncio.to_thread(rag.search, "warm up")  # load corpus, index and embedder before the first request
    yield


app = FastAPI(title="mini-wiki RAG", lifespan=lifespan)


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    k: int = Field(default=5, ge=1, le=10)


class Source(BaseModel):
    id: int
    score: float
    text: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    model: str
    latency_ms: int


_hits: dict[str, list[float]] = defaultdict(list)


def auth_and_limit(authorization: str = Header(default="")) -> str:
    key = authorization.removeprefix("Bearer ").strip()
    if key not in API_KEYS:
        raise HTTPException(401, "invalid or missing API key")
    # ponytail: in-memory sliding window, per process. Multiple instances need a shared store (Redis) or the gateway's limiter.
    now = time.time()
    _hits[key] = [t for t in _hits[key] if now - t < 60]
    if len(_hits[key]) >= RATE_PER_MIN:
        raise HTTPException(429, "rate limit exceeded", headers={"Retry-After": "60"})
    _hits[key].append(now)
    return key


async def _retrieve(req: AskRequest):
    hits = await asyncio.to_thread(rag.search, req.question, req.k)  # CPU-bound embedding: keep it off the event loop
    sources = "\n\n".join(f"[{i}] {text}" for i, _, text in hits)
    messages = [{"role": "user", "content": rag.PROMPT.format(sources=sources, question=req.question)}]
    return hits, messages


@app.get("/healthz")
async def healthz():
    return {"status": "ok", "model": MODEL}


@app.post("/v1/ask", response_model=AskResponse)
async def ask(req: AskRequest, _key: str = Depends(auth_and_limit)):
    start = time.perf_counter()
    hits, messages = await _retrieve(req)
    try:
        r = await llm.chat.completions.create(model=MODEL, messages=messages, temperature=0, max_tokens=400, **EXTRA)
    except Exception as e:
        raise HTTPException(502, f"LLM provider error: {type(e).__name__}") from e
    return AskResponse(answer=r.choices[0].message.content, model=MODEL, latency_ms=int((time.perf_counter() - start) * 1000),
                       sources=[Source(id=i, score=round(s, 3), text=t[:300]) for i, s, t in hits])


@app.post("/v1/ask/stream")
async def ask_stream(req: AskRequest, _key: str = Depends(auth_and_limit)):
    """Server-Sent Events: one `sources` event, then `token` events, then `done` (or `error`)."""
    hits, messages = await _retrieve(req)

    async def events():
        yield f"event: sources\ndata: {json.dumps([{'id': i, 'score': round(s, 3)} for i, s, _ in hits])}\n\n"
        try:
            stream = await llm.chat.completions.create(model=MODEL, messages=messages, temperature=0, max_tokens=400, stream=True, **EXTRA)
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield f"event: token\ndata: {json.dumps(chunk.choices[0].delta.content)}\n\n"
            yield "event: done\ndata: {}\n\n"
        except Exception as e:  # headers are already sent: report the failure in-band
            yield f"event: error\ndata: {json.dumps(type(e).__name__)}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})

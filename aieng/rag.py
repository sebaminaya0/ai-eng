"""The minimal RAG pipeline built in 08.01, packaged so chapters 08-11 can reuse it.

    from aieng import rag
    rag.search("Who was Abraham Lincoln?")      # [(passage_id, score, text), ...]
    text, hits = rag.answer("Who was Abraham Lincoln?")
"""
from functools import lru_cache

import numpy as np

from aieng import DATA
from aieng.llm import chat

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "  # bge models want this on queries only


def _fix_mojibake(text):
    """Some passages are UTF-8 that was decoded as Latin-1 ("â\x80\x93" instead of "–"). Real data is dirty."""
    try:
        return text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


@lru_cache
def corpus() -> list[str]:
    from datasets import load_dataset
    return [_fix_mojibake(p) for p in load_dataset("rag-datasets/rag-mini-wikipedia", "text-corpus")["passages"]["passage"]]


@lru_cache
def qa() -> list[dict]:
    from datasets import load_dataset
    return list(load_dataset("rag-datasets/rag-mini-wikipedia", "question-answer")["test"])


@lru_cache
def eval_set() -> list[dict]:
    """Questions with a non-trivial answer string, plus 'gold' passages = those containing that string.
    ponytail: proxy relevance labels (string match); hand-label passages for a real eval (chapter 10)."""
    docs = [d.lower() for d in corpus()]
    out = []
    for row in qa():
        ans = row["answer"].strip().rstrip(".").lower()
        if len(ans) < 4 or ans in ("yes", "no"):
            continue
        gold = {i for i, d in enumerate(docs) if ans in d}
        if gold:
            out.append({**row, "gold": gold})
    return out


@lru_cache
def embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBED_MODEL)


def embed(texts, query=False):
    texts = [QUERY_PREFIX + t for t in texts] if query else list(texts)
    return embedder().encode(texts, normalize_embeddings=True, batch_size=64)


@lru_cache
def index() -> np.ndarray:
    path = DATA / f"mini-wiki-v2-{EMBED_MODEL.replace('/', '_')}.npy"  # v2: after mojibake fix
    if not path.exists():
        np.save(path, embed(corpus()))
    return np.load(path)


def search(query, k=5):
    """[(passage_id, score, text)] by cosine similarity (vectors are normalised, so dot product)."""
    scores = index() @ embed([query], query=True)[0]
    top = np.argsort(-scores)[:k]
    docs = corpus()
    return [(int(i), float(scores[i]), docs[i]) for i in top]


PROMPT = """Answer the question using only the sources below. Cite the sources you use like [12].
If the sources don't contain the answer, say "I don't know".

{sources}

Question: {question}"""


def answer(question, k=5, **chat_kwargs):
    hits = search(question, k)
    sources = "\n\n".join(f"[{i}] {text}" for i, _, text in hits)
    return chat(PROMPT.format(sources=sources, question=question), temperature=0, **chat_kwargs), hits

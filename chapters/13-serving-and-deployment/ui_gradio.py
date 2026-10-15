"""Gradio chat UI for the 13.03 API (streams over SSE). Built in 13.04.

    uv run uvicorn app:app --port 8765 &      # the API
    uv run python ui_gradio.py                # UI on http://localhost:7860
"""
import json
import os

import gradio as gr
import httpx

API_URL = os.getenv("API_URL", "http://localhost:8765")
API_KEY = os.getenv("API_KEY", "dev-key")


def stream_answer(question):
    """Yield (text so far, source ids) from the API's SSE stream."""
    text, sources, event = "", [], None
    with httpx.stream("POST", f"{API_URL}/v1/ask/stream", json={"question": question},
                      headers={"Authorization": f"Bearer {API_KEY}"}, timeout=60) as r:
        if r.status_code != 200:
            r.read()
            yield f"⚠️ API error {r.status_code}: {r.json().get('detail', '')}", []
            return
        for line in r.iter_lines():
            if line.startswith("event: "):
                event = line[7:]
            elif line.startswith("data: "):
                data = json.loads(line[6:])
                if event == "sources":
                    sources = [s["id"] for s in data]
                elif event == "token":
                    text += data
                    yield text, sources
                elif event == "error":
                    yield text + f"\n\n⚠️ {data}", sources


def respond(message, history):
    text, sources = "", []
    for text, sources in stream_answer(message):
        yield text
    yield (text or "(the model returned an empty answer — try again)") + f"\n\n<sub>sources: {', '.join(map(str, sources))}</sub>"


demo = gr.ChatInterface(respond, title="mini-wiki RAG", description="Answers from 3.2k Wikipedia passages, with citations.",
                        examples=["Who was Abraham Lincoln?", "What is the capital of Uruguay?"])

if __name__ == "__main__":
    demo.launch()

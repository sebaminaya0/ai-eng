"""One process, one port: the 13.03 API plus the 13.04 Gradio UI mounted at /ui. This is what 13.05 deploys.

    PORT=7860 uv run uvicorn serve:app --port 7860     # API at /v1/..., UI at /ui
"""
import os

os.environ.setdefault("API_URL", f"http://localhost:{os.getenv('PORT', '7860')}")  # the UI calls the API in the same process
os.environ.setdefault("API_KEY", os.getenv("APP_API_KEYS", "dev-key").split(",")[0])

import gradio as gr
from fastapi.responses import RedirectResponse

from app import app
from ui_gradio import demo


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/ui")


app = gr.mount_gradio_app(app, demo, path="/ui")

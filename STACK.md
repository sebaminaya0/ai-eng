# The AI Engineering Stack

Every layer has substitutes. The repo teaches the **default** first (free, common, easy to run locally), then makes you try the main alternatives so you can choose for real projects. Tools move fast: re-check this table every few months.

Legend: **F** free / open source · **FT** free tier · **P** paid

## 1. Foundations

| Layer | Default | Alternatives | Chapter |
|---|---|---|---|
| Language | Python 3.12 (F) | TypeScript for front-ends/agents (Vercel AI SDK, Mastra) | 01 |
| Env / packages | uv (F) | pip + venv, conda/mamba, poetry | 00 |
| Notebooks | VS Code + Jupyter (F) | JupyterLab, Colab (FT), Kaggle (FT), Cursor | 00 |
| Data | pandas (F) | polars, DuckDB | 01 |
| Classic ML | scikit-learn (F) | XGBoost, LightGBM, CatBoost | 02 |
| DL framework | PyTorch (F) | JAX/Flax, TensorFlow/Keras, MLX (Apple Silicon) | 03 |
| Model hub | Hugging Face (F) | Ollama library, ModelScope, Kaggle Models | 04 |

## 2. Models

| Layer | Default | Alternatives | Chapter |
|---|---|---|---|
| Closed frontier APIs | Gemini Flash (FT) | OpenAI (P), Anthropic Claude (P), xAI Grok (P), Mistral (FT/P) | 05 |
| Hosted open-weight | Groq (FT) | OpenRouter (FT `:free`), Together (P), Fireworks (P), Cerebras (FT), DeepInfra (P) | 05 |
| Local runtime | Ollama (F) | LM Studio, llama.cpp, MLX-LM, vLLM (GPU) | 05, 13 |
| Open-weight families | Qwen, Llama, Gemma (F) | Mistral, DeepSeek, gpt-oss, Phi, SmolLM | 04 |
| Embeddings | sentence-transformers / BGE (F) | OpenAI, Gemini, Voyage, Cohere, Nomic, Qwen3-Embedding | 07 |
| Rerankers | bge-reranker (F) | Cohere Rerank (FT/P), Voyage, ColBERT | 07 |

## 3. Application layer

| Layer | Default | Alternatives | Chapter |
|---|---|---|---|
| LLM client | `openai` SDK on OpenAI-compatible endpoints (F) | native `anthropic` / `google-genai` SDKs, LiteLLM, aisuite | 05 |
| Structured output | Pydantic + native structured outputs (F) | Instructor, Outlines, BAML | 05 |
| Prompt optimisation | hand-written + evals | DSPy | 06 |
| Doc parsing | PyMuPDF / MarkItDown (F) | Docling, Unstructured, LlamaParse (P), Reducto (P) | 08 |
| Vector store | Chroma (F) | LanceDB, Qdrant (local mode or server), sqlite-vec, pgvector, Weaviate, Milvus, Pinecone (FT/P), FAISS (library) | 07 |
| Lexical search | bm25s (F) | Elasticsearch/OpenSearch, Postgres FTS, Tantivy | 07 |
| RAG framework | none (from scratch) first | LangChain, LlamaIndex, Haystack | 08 |
| Agent framework | from scratch first, then LangGraph (F) | OpenAI Agents SDK, Claude Agent SDK, Google ADK, PydanticAI, smolagents, CrewAI, Microsoft Agent Framework | 09 |
| Tool protocol | MCP (F) | provider-native function calling | 09 |
| Sandboxes | restricted interpreter + subprocess limits (F, not a security boundary) | Docker, E2B (FT), Modal (FT), Daytona, Pyodide/WASM | 09 |

## 4. Quality & operations

| Layer | Default | Alternatives | Chapter |
|---|---|---|---|
| Evals | own pytest-style evals + promptfoo + Inspect AI (F) | DeepEval, Ragas (run isolated: they conflict with this repo's pins), Braintrust (FT), LangSmith/Langfuse datasets | 10 |
| Tracing / observability | Arize Phoenix, local in-process (F) | Langfuse (self-host F / cloud FT), LangSmith (FT), W&B Weave (FT), Logfire (FT), Helicone (FT), Opik | 11 |
| Gateway / routing | LiteLLM proxy (F) | OpenRouter, Portkey, Cloudflare AI Gateway | 11 |
| Guardrails | Presidio + Llama Guard (F) | NeMo Guardrails, Guardrails AI, provider moderation APIs | 11 |

## 5. Training & serving

| Layer | Default | Alternatives | Chapter |
|---|---|---|---|
| Fine-tuning | HF TRL + PEFT on Mac (MPS) and MLX-LM (F) | Unsloth on Colab/Kaggle free GPUs, Axolotl, LLaMA-Factory, managed FT (OpenAI, Together — P) | 12 |
| Experiment tracking | W&B (FT) | MLflow, TensorBoard, Trackio | 12 |
| Quantization | Ollama `--quantize int4/int8` + MLX quants on Mac (F) | GGUF via llama.cpp (k-quants), AWQ, GPTQ, bitsandbytes, FP8/NVFP4/MXFP4 (GPU) | 13 |
| Inference server | Ollama / MLX-LM server locally; vLLM on GPUs (F) | SGLang, TensorRT-LLM, llama.cpp server, TGI (maintenance mode) | 13 |
| API | FastAPI (F) | Litestar, Flask, LangServe | 13 |
| UI | Gradio (F) | Streamlit, Chainlit, Open WebUI, Next.js + Vercel AI SDK | 13 |
| Hosting | Hugging Face Docker Spaces (FT; built remotely, no local Docker) | Modal (FT), Render, Fly.io, Railway, Cloud Run, RunPod (P), AWS Bedrock / GCP Vertex / Azure AI Foundry (P) | 13 |

## 6. Multimodal

| Layer | Default | Alternatives | Chapter |
|---|---|---|---|
| Vision-language | Gemini Flash (FT) + Qwen3-VL 2B on Ollama (F) | GPT, Claude, Gemma, InternVL, SmolVLM, mlx-vlm | 14 |
| Speech-to-text | mlx-whisper on Mac (F) + Groq Whisper API (FT) | faster-whisper, whisper.cpp, Parakeet, Deepgram (FT), AssemblyAI (FT), OpenAI (P) | 14 |
| Text-to-speech | Kokoro (F) | ElevenLabs (P), OpenAI TTS (P) | 14 |
| Voice agents | cascaded pipeline from scratch, then Pipecat (F) | LiveKit Agents, OpenAI Realtime / Gemini Live | 14 |
| Image generation | diffusers + SD-Turbo (F) | FLUX, SD 3.5, Qwen-Image, ComfyUI, API models (Gemini/Imagen, GPT-Image) | 14 |
| Multimodal retrieval | ColPali family (ColSmol) + VLM captions (F) | CLIP/SigLIP, Byaldi, multi-vector DBs (Vespa, Qdrant, LanceDB) | 14 |

## Version gotchas found while building the lessons (Oct 2026)
- `mcp` 2.x renamed `FastMCP` → `MCPServer` (`from mcp.server.mcpserver import MCPServer`) and snake_cased fields (`input_schema`).
- Haystack 3.x moved its sentence-transformers embedders out of core (08.03 uses a 6-line custom component instead).
- TRL 1.15 trainers require a Triton (Linux-only) fused LM head → pinned `trl<1.15` for macOS.
- Ollama's OpenAI-compatible API ignores `tool_choice`; agent loops nudge instead (08.06, 09.x).
- Ollama 0.40 `--quantize` takes `int4`/`int8`/`nvfp4`/`mxfp4`/`mxfp8` (not `q8_0`), and importing safetensors ignores HF's `chat_template` →
  always set `TEMPLATE` in the Modelfile (12.06, 13.01).
- transformers 5 loads weights in parallel threads; with `device_map` on MPS (e.g. `lm_eval`) that segfaults → `HF_DEACTIVATE_ASYNC_LOAD=1`.
- `qwen3-vl:2b` is the *thinking* variant and ignores `reasoning_effort` → use `qwen3-vl:2b-instruct`. Ollama raw `/api/generate` on thinking
  models returns text in `thinking` unless `"think": false` (15.01).
- `colpali-engine` pins `torch<2.14` and `peft<0.21` → run it isolated (14.05). Hugging Face Xet downloads can stall: `HF_HUB_DISABLE_XET=1`.
- Gradio 6 names a `ChatInterface` API endpoint after the function (`/respond`); Streamlit `AppTest.from_file` needs an absolute path in notebooks.
- Groq model ids come and go (e.g. `llama-3.1-8b-instant` is gone; `openai/gpt-oss-20b` / `-120b` available): list them with `client.models.list()`.
- `arize-phoenix` needs `graphql-core<3.3`. Ragas 0.4.3, DeepEval and current Inspect AI (needs openai>=3.4) conflict with this env: run them with `uv run --isolated --with ...`.

## Where money might be unavoidable
- **Frontier closed models** (OpenAI/Anthropic) for comparisons: ~$5–20 total covers the whole course if you keep tests small. Optional; free tiers do most work.
- **GPU beyond free quotas** (chapter 12 larger runs, 13.02 vLLM, 15.02 nanochat): rent by the hour (RunPod/Modal/Lambda), usually a few dollars per experiment.
  Deploying (13.05) is free on Hugging Face Spaces.
- **Book (optional, best single reference):** Chip Huyen, *AI Engineering* (O'Reilly, 2025).

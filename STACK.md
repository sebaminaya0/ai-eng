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
| Vector store | Chroma (F) | LanceDB, Qdrant, Weaviate, Milvus, pgvector, Pinecone (FT/P), FAISS (library) | 07 |
| Lexical search | bm25s (F) | Elasticsearch/OpenSearch, Postgres FTS, Tantivy | 07 |
| RAG framework | none (from scratch) first | LangChain, LlamaIndex, Haystack | 08 |
| Agent framework | from scratch first, then LangGraph (F) | OpenAI Agents SDK, Claude Agent SDK, Google ADK, PydanticAI, smolagents, CrewAI, Microsoft Agent Framework | 09 |
| Tool protocol | MCP (F) | provider-native function calling | 09 |
| Sandboxes | Docker (F) | E2B (FT), Modal (FT), Daytona | 09 |

## 4. Quality & operations

| Layer | Default | Alternatives | Chapter |
|---|---|---|---|
| Evals | own pytest-style evals + promptfoo (F) | DeepEval, Ragas, Inspect AI, Braintrust (FT), LangSmith/Langfuse datasets | 10 |
| Tracing / observability | Langfuse self-hosted (F) | LangSmith (FT), Arize Phoenix (F), W&B Weave (FT), Logfire (FT), Helicone (FT) | 11 |
| Gateway / routing | LiteLLM proxy (F) | OpenRouter, Portkey, Cloudflare AI Gateway | 11 |
| Guardrails | Presidio + Llama Guard (F) | NeMo Guardrails, Guardrails AI, provider moderation APIs | 11 |

## 5. Training & serving

| Layer | Default | Alternatives | Chapter |
|---|---|---|---|
| Fine-tuning | Unsloth on Colab/Kaggle (F) | HF TRL + PEFT, Axolotl, LLaMA-Factory, MLX-LM, managed FT (OpenAI, Together — P) | 12 |
| Experiment tracking | W&B (FT) | MLflow, TensorBoard, Trackio | 12 |
| Quantization | GGUF via llama.cpp (F) | AWQ, GPTQ, bitsandbytes, MLX quants | 13 |
| Inference server | vLLM (F) | SGLang, TGI, TensorRT-LLM, llama.cpp server, Ollama | 13 |
| API | FastAPI (F) | Litestar, Flask, LangServe | 13 |
| UI | Gradio (F) | Streamlit, Chainlit, Open WebUI, Next.js + Vercel AI SDK | 13 |
| Hosting | Hugging Face Spaces (FT) | Modal (FT), Render, Fly.io, Railway, Cloud Run, RunPod (P), AWS Bedrock / GCP Vertex / Azure AI Foundry (P) | 13 |

## 6. Multimodal

| Layer | Default | Alternatives | Chapter |
|---|---|---|---|
| Vision-language | Gemini Flash (FT) | GPT, Claude, Qwen-VL, Gemma, SmolVLM | 14 |
| Speech-to-text | faster-whisper (F) | Deepgram (FT), AssemblyAI (FT), OpenAI (P) | 14 |
| Text-to-speech | Kokoro (F) | ElevenLabs (P), OpenAI TTS (P) | 14 |
| Voice agents | Pipecat (F) | LiveKit Agents, realtime APIs | 14 |
| Image generation | diffusers (F) | ComfyUI, API models | 14 |

## Where money might be unavoidable
- **Frontier closed models** (OpenAI/Anthropic) for comparisons: ~$5–20 total covers the whole course if you keep tests small. Optional; free tiers do most work.
- **GPU beyond free quotas** (chapter 12 larger runs, chapter 15 pretraining): rent by the hour (RunPod/Modal/Lambda), usually a few dollars per experiment.
- **Book (optional, best single reference):** Chip Huyen, *AI Engineering* (O'Reilly, 2025).

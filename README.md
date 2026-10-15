# AI Engineering — from fundamentals to frontier

Self-study curriculum: 17 chapters, ~90 lessons, one Jupyter notebook each. Free resources first; paid only where unavoidable (see [STACK.md](STACK.md#where-money-might-be-unavoidable)).

- [STACK.md](STACK.md) — every layer of the stack, default choice and main alternatives.
- `chapters/` — lessons. Each notebook has goals, resources, notes, exercises.

## Setup (macOS)
```bash
brew install ollama libomp          # local LLMs; libomp is needed by LightGBM/XGBoost
brew services start ollama && ollama pull qwen3:1.7b
uv sync
uv run python -m ipykernel install --user --name ai-eng
cp .env.example .env                # optional: free keys for Gemini, Groq, OpenRouter
```
Then open `chapters/00-setup/01-welcome.ipynb`.

Every lesson runs with **zero API keys** on local Ollama. The `aieng` package holds the little shared code: `aieng.DATA`
(git-ignored `data/` folder) and `aieng.llm` (one OpenAI-compatible client for every provider; pick with `AIENG_PROVIDER` in `.env`).

## Curriculum

| # | Chapter | What you learn | Core free resources |
|---|---|---|---|
| 00 | Setup | Env, tooling, first LLM call from multiple providers | — |
| 01 | Python & Math | async Python, NumPy, linear algebra, probability, gradients | 3Blue1Brown, MML book |
| 02 | ML Fundamentals | regression, metrics, overfitting, trees, clustering | Google ML Crash Course, Andrew Ng (audit) |
| 03 | Deep Learning | autograd, PyTorch (vs JAX/MLX), training | Karpathy Zero to Hero, fast.ai, d2l.ai |
| 04 | Transformers & LLMs | tokenization, attention, tiny GPT, how LLMs are trained | Karpathy, CS336, HF LLM Course |
| 05 | LLM APIs | providers, chat/streaming, structured outputs, cost, local models | provider docs, Ollama |
| 06 | Prompt & Context Eng. | prompting, reasoning, templates, context engineering, DSPy | Anthropic tutorial, promptingguide.ai |
| 07 | Embeddings & Vector Search | embeddings, ANN, vector DBs, BM25/hybrid, rerankers | Pinecone Learn, MTEB, sbert.net |
| 08 | RAG | from scratch, parsing/chunking, frameworks, advanced retrieval, GraphRAG | LLM Zoomcamp |
| 09 | Agents | tool calling, agent loop, patterns, MCP, frameworks, multi-agent | HF Agents & MCP courses, LangChain Academy |
| 10 | Evals | error analysis, datasets, LLM-as-judge, RAG/agent evals, CI | Hamel Husain, promptfoo, Inspect |
| 11 | LLMOps & Safety | tracing, gateways, prompt injection, guardrails, feedback loops | Langfuse, OWASP GenAI |
| 12 | Fine-tuning | when to, data, LoRA/QLoRA, DPO, GRPO, export | Unsloth, TRL, mlabonne/llm-course |
| 13 | Serving & Deployment | quantization, vLLM/SGLang, FastAPI, UIs, hosting, cost | vLLM docs, HF Spaces, FSDL |
| 14 | Multimodal | VLMs, speech, voice agents, diffusion, multimodal RAG | HF Audio & Diffusion courses |
| 15 | Advanced | reasoning models, pretrain small LLM, distillation, interpretability, long-running agents | nanochat, CS336, ARENA |
| 16 | Capstone | ship a real product end to end | — |

Suggested order is linear. Shortcut for experienced devs: 00 → 04 (skim 01-03) → 05 onwards, back-filling fundamentals when stuck.

## Milestones

Each milestone is a portfolio project. Tick when done.

- [ ] **M0 — Ready** (ch 00): environment works, two free providers answer from a notebook.
- [ ] **M1 — Foundations** (ch 01-04): char-level GPT trained from scratch on your own text; you can explain attention and backprop on a whiteboard.
- [ ] **M2 — LLM builder** (ch 05-06): streaming CLI assistant, provider-swappable, structured outputs, retries, cost log, runs locally via Ollama too.
- [ ] **M3 — Retrieval** (ch 07-08): Q&A over your own documents with hybrid search + reranking + citations, retrieval recall measured.
- [ ] **M4 — Agents** (ch 09): agent with ≥3 tools, your own MCP server, memory and human approval for risky actions.
- [ ] **M5 — Production** (ch 10, 11, 13): M3 or M4 app deployed publicly with eval suite in CI, tracing, guardrails, cost/latency dashboard.
- [ ] **M6 — Model customization** (ch 12): fine-tuned small model that beats its base on your eval, exported to GGUF, served locally.
- [ ] **M7 — Frontier & capstone** (ch 14-16): multimodal or voice feature, one advanced deep-dive, capstone shipped with a public write-up.

## Rough time budget (part-time, ~10 h/week)
M0: 1 week · M1: 6-10 weeks · M2: 2 weeks · M3: 3 weeks · M4: 3 weeks · M5: 4 weeks · M6: 3 weeks · M7: open-ended.

## How lessons grow
Chapters 00–06 are fully written and verified end to end on an Apple Silicon Mac (explanations, runnable code, exercises).
Chapters 07–16 are stubs (goals, curated resources, exercises): ask Claude to flesh out the next chapter when you reach it.

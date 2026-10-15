"""One OpenAI-compatible client for every provider. Built in 00.03, reused from chapter 05 on.

    from aieng.llm import chat, client
    chat("Hello")                        # first configured provider
    chat("Hello", provider="groq")       # explicit
    c, model = client("ollama")          # raw OpenAI client for full control

Pick a default with AIENG_PROVIDER / AIENG_MODEL in .env.
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# name: (base_url, api-key env var, default model). Model ids change: check provider docs.
PROVIDERS = {
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/", "GEMINI_API_KEY", "gemini-flash-lite-latest"),
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY", "openai/gpt-oss-120b"),
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", "openrouter/free"),
    "openai": ("https://api.openai.com/v1", "OPENAI_API_KEY", "gpt-5-mini"),
    "ollama": ("http://localhost:11434/v1", None, os.getenv("OLLAMA_MODEL", "qwen3:1.7b")),
}


def available():
    """Providers with a key set (ollama always listed; it may still not be running)."""
    return [n for n, (_, key, _) in PROVIDERS.items() if key is None or os.getenv(key)]


def client(provider=None):
    """Return (OpenAI client, default model) for a provider."""
    provider = provider or os.getenv("AIENG_PROVIDER") or available()[0]
    base_url, key_var, model = PROVIDERS[provider]
    api_key = os.getenv(key_var) if key_var else "ollama"
    return OpenAI(base_url=base_url, api_key=api_key, timeout=120), os.getenv("AIENG_MODEL") or model


def chat(prompt_or_messages, provider=None, model=None, system=None, **kwargs):
    """Send a prompt (str) or a messages list, return the reply text."""
    messages = prompt_or_messages
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    if system:
        messages = [{"role": "system", "content": system}, *messages]
    c, default_model = client(provider)
    if c.base_url.host == "localhost":
        kwargs.setdefault("reasoning_effort", "none")  # qwen3 & co. think by default: slow on a laptop
    resp = c.chat.completions.create(model=model or default_model, messages=messages, **kwargs)
    return resp.choices[0].message.content

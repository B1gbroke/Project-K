# src/nlp/llm.py
from typing import List, Dict
import requests
from src.core.config import config

Conversation = List[Dict[str, str]]

def _build_prompt(user_text: str, history: Conversation) -> str:
    """
    Turn conversation history into a single text prompt
    for /api/generate.
    """
    lines = [
        "You are a helpful, concise voice assistant. "
        "Respond conversationally and keep answers fairly short.\n"
    ]

    for msg in history:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "user":
            lines.append(f"User: {content}")
        elif role == "assistant":
            lines.append(f"Assistant: {content}")

    lines.append(f"User: {user_text}")
    lines.append("Assistant:")
    return "\n".join(lines)

def _call_ollama_generate(user_text: str, history: Conversation) -> str:
    """Call Ollama's /api/generate endpoint (non-streaming)."""
    url = f"{config.OLLAMA_HOST}/api/generate"
    prompt = _build_prompt(user_text, history)

    payload = {
        "model": config.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,   # get one JSON response instead of a stream
    }

    print(f"[LLM] Sending request to Ollama at {url} ...")
    resp = requests.post(url, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()

    # /api/generate returns a single JSON object with a "response" field
    reply = (data.get("response") or "").strip()
    if not reply:
        reply = "(empty reply from model)"
    return reply

def generate_reply(user_text: str, history: Conversation | None = None) -> str:
    """
    Take the user's text + optional history and return an assistant reply.
    Uses Ollama running locally on the Pi.
    """
    history = history or []
    backend = config.LLM_BACKEND

    if backend == "ollama":
        try:
            return _call_ollama_generate(user_text, history)
        except Exception as e:
            print(f"[LLM] Error calling Ollama: {e}")
            return f"(LLM error: {e})"

    # Fallback if backend misconfigured
    print(f"[LLM] Unknown backend {backend}, using stub.")
    return f"You said: {user_text}. (LLM backend not configured.)"

"""Talks to Qwen3 8B via a local Ollama server. Knows nothing about Neo4j."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:8b")


def verify_ollama():
    """Raises a clear error if Ollama is unreachable or the model is missing."""
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_HOST}. Start it with `ollama serve` "
            "or open the Ollama app."
        ) from e

    models = [m["name"] for m in resp.json().get("models", [])]
    if OLLAMA_MODEL not in models:
        raise RuntimeError(
            f"Model '{OLLAMA_MODEL}' is not available in Ollama. "
            f"Run: ollama pull {OLLAMA_MODEL}\nAvailable models: {models}"
        )
    return True


def ask_qwen(system_prompt: str, user_prompt: str, think: bool | None = None,
             timeout: int = 120) -> str:
    """Sends a system + user prompt to Qwen3 8B and returns the plain text answer.

    `think=False` turns off Qwen3's reasoning pass. For tasks that only reformat
    supplied context -- listing question papers and their links, say -- the
    reasoning pass is pure latency, so callers doing that pass think=False.
    Leaving it as None keeps Ollama's default, so existing callers are unchanged.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
    }
    if think is not None:
        payload["think"] = think

    try:
        resp = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload,
                             timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_HOST}. Is it running?"
        ) from e
    except requests.exceptions.Timeout as e:
        raise RuntimeError("Ollama took too long to respond (timeout).") from e

    payload = resp.json()
    message = payload.get("message", {})
    content = message.get("content")
    if not content:
        raise RuntimeError(f"Malformed response from Ollama: {payload}")
    return content.strip()

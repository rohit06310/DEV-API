"""
utils/groq_client.py
──────────────────────────────────────────────────
Singleton Groq client + model configuration.
All LLM calls in the project must go through this module.
"""
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ── Model selection ────────────────────────────────────────────────────────────
# llama-3.3-70b-versatile:
#   • 128k context window — handles large HTML documentation pages
#   • Best in class at structured JSON output and code generation
#   • Versatile across extraction, analysis, and synthesis tasks
#   • Ideal for this project's dual needs: JSON parsing + SDK codegen
GROQ_MODEL_PRIMARY  = "llama-3.3-70b-versatile"

# Fallback model (smaller, faster — used if primary fails or for quick tasks)
GROQ_MODEL_FALLBACK = "llama3-8b-8192"

_API_KEY = os.environ.get("GROQ_API_KEY", "")

def get_client() -> Groq | None:
    """Return the configured Groq client, or None if key is missing."""
    if not _API_KEY:
        return None
    return Groq(api_key=_API_KEY)


def chat_completion(
    messages: list[dict],
    json_mode: bool = False,
    max_tokens: int = 4096,
    temperature: float = 0.1,
    use_fallback: bool = False,
) -> str | None:
    """
    Central wrapper for all Groq chat completions.

    Args:
        messages:     OpenAI-style messages list.
        json_mode:    If True, enforces JSON object response format.
        max_tokens:   Maximum tokens in the response.
        temperature:  Sampling temperature (lower = more deterministic).
        use_fallback: If True, uses the smaller fallback model instead.

    Returns:
        The raw text content of the response, or None on failure.
    """
    client = get_client()
    if not client:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env file.")

    model = GROQ_MODEL_FALLBACK if use_fallback else GROQ_MODEL_PRIMARY

    kwargs: dict = {
        "model":      model,
        "messages":   messages,
        "temperature": temperature,
        "max_tokens":  max_tokens,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    try:
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        # Try fallback model on primary failure
        if not use_fallback:
            try:
                kwargs["model"] = GROQ_MODEL_FALLBACK
                response = client.chat.completions.create(**kwargs)
                return response.choices[0].message.content
            except Exception:
                pass
        raise RuntimeError(f"Groq API call failed: {e}") from e

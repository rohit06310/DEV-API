"""
utils/sdk_generator.py
──────────────────────────────────────────────────
SDK / wrapper code generator.
Takes a structured APISpec and generates clean,
production-ready code in the requested language and style.

Completely decoupled from the UI layer.
"""
import re
from utils.groq_client import chat_completion


# ── Supported languages ───────────────────────────────────────────────────────
SUPPORTED_LANGUAGES = ["Python", "JavaScript", "TypeScript", "Java", "Go", "cURL"]
LANG_EXTENSIONS     = {
    "Python":     "py",
    "JavaScript": "js",
    "TypeScript": "ts",
    "Java":       "java",
    "Go":         "go",
    "cURL":       "sh",
}

# ── Prompts ───────────────────────────────────────────────────────────────────
_SYSTEM_PROMPT = """\
You are a senior software engineer writing production-quality API client code.
You write clean, idiomatic, well-commented code exactly as a professional engineer would.
You NEVER include markdown code fences, preamble text, or closing remarks.
You output ONLY the raw source code — nothing else.\
"""

_STYLE_INSTRUCTIONS = {
    "Minimal Functions": (
        "Write simple, standalone functions only. "
        "No classes, no __init__, no setup boilerplate. "
        "Each function should be directly callable with minimal configuration."
    ),
    "Wrapper Class": (
        "Write a well-structured object-oriented API client class. "
        "Include a constructor/initializer that accepts the base URL and auth token. "
        "Include typed method signatures, docstrings, and proper HTTP error handling. "
        "The class should be immediately usable in a production codebase."
    ),
}


def _build_prompt(
    api_name:       str,
    base_url:       str,
    auth_headers:   dict,
    lang:           str,
    style:          str,
    endpoint_target: str,
) -> str:
    style_instr = _STYLE_INSTRUCTIONS.get(style, _STYLE_INSTRUCTIONS["Minimal Functions"])

    ep_instr = (
        f"Focus specifically on this endpoint: '{endpoint_target}'. "
        f"Ensure there is a clearly named, dedicated function/method for it. "
        f"You may include 1-2 closely related endpoints for context."
        if endpoint_target and endpoint_target != "Full API Integration"
        else "Cover the most commonly used endpoints comprehensively."
    )

    return f"""Write a {lang} API client for the following API:

API Name:    {api_name}
Base URL:    {base_url}
Auth Headers: {auth_headers}

Target: {ep_instr}
Style:  {style_instr}

STRICT OUTPUT RULES:
1. Output ONLY raw {lang} code. No exceptions.
2. NO markdown code fences (no backticks anywhere).
3. NO introductory sentences, NO closing remarks.
4. NO comments referencing AI, code generation, or tools.
5. DO include brief inline comments explaining non-obvious logic.
6. Handle HTTP errors with clear error messages (raise exceptions / return error objects).
7. Make the code immediately usable — include import statements at the top.
"""


def _clean_code_output(text: str) -> str:
    """Strip any accidental markdown fences from LLM output."""
    text = text.strip()
    # Remove ```language fence at start
    text = re.sub(r"^```[a-zA-Z]*\s*\n?", "", text)
    # Remove ``` at end
    text = re.sub(r"\n?```\s*$", "", text)
    # Final cleanup
    text = text.replace("```", "").strip()
    return text


# ── Public API ─────────────────────────────────────────────────────────────────

def generate_sdk(
    api_name:        str,
    base_url:        str,
    auth_headers:    dict,
    lang:            str,
    style:           str,
    endpoint_target: str = "",
) -> str:
    """
    Generate SDK/wrapper code for an API.

    Args:
        api_name:        Human-readable API name.
        base_url:        Full API base URL.
        auth_headers:    Dict of required auth headers.
        lang:            Target programming language.
        style:           "Minimal Functions" or "Wrapper Class".
        endpoint_target: Specific endpoint to focus on (e.g. "POST /payments").

    Returns:
        Raw source code string.

    Raises:
        RuntimeError: If the Groq API is not configured or call fails.
        ValueError:   If an unsupported language is requested.
    """
    if lang not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: '{lang}'. Choose from {SUPPORTED_LANGUAGES}.")

    prompt = _build_prompt(api_name, base_url, auth_headers, lang, style, endpoint_target)

    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user",   "content": prompt},
    ]

    raw = chat_completion(
        messages=messages,
        json_mode=False,
        max_tokens=2048,
        temperature=0.15,
    )

    if not raw:
        return f"# SDK generation failed. Please check your Groq API key and try again."

    return _clean_code_output(raw)

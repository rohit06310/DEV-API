"""
utils/parser.py
──────────────────────────────────────────────────
API documentation parser.
Takes a raw documentation URL + optional use case,
fetches the page text, calls the LLM, and returns
a clean, validated APISpec dict.

This is the single source of truth for structured
API data in the entire DevFlow application.
"""
import json
import re
from typing import TypedDict

from utils.groq_client import chat_completion
from utils.scraper import fetch_doc_text


# ── Output schema (TypedDict for type safety) ─────────────────────────────────

class Endpoint(TypedDict):
    method:      str   # HTTP method: GET, POST, PUT, DELETE, PATCH
    path:        str   # Endpoint path: /resource/{id}
    description: str   # Short description of what the endpoint does
    params:      str   # Key query/path params (comma-separated) or "None"


class APISpec(TypedDict):
    api_name:       str
    version:        str
    base_url:       str
    description:    str
    auth_method:    str
    auth_headers:   dict[str, str]   # {"Header-Name": "example-value"}
    auth_example:   str              # curl command
    rate_limits:    str
    endpoints:      list[Endpoint]
    use_cases:      list[str]
    research_notes: str


# ── Prompt ────────────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """\
You are an expert API analyst and technical documentation parser.
Your job is to extract structured API metadata from documentation pages.
You ALWAYS return valid JSON. You NEVER add any text outside the JSON object.\
"""

_USER_PROMPT_TEMPLATE = """\
Analyse the REST API documentation at this URL: {url}

{page_context}{use_case_context}

Return ONLY a valid JSON object matching this schema exactly — no markdown, no extra text:

{{
  "api_name":       "string — human-readable API name",
  "version":        "string — API version e.g. v1, v2 or 'N/A'",
  "base_url":       "string — full base URL including version prefix if any",
  "description":    "string — 2-3 sentences describing what this API does",
  "auth_method":    "string — e.g. Bearer Token, API Key in Header, OAuth 2.0, Basic Auth",
  "auth_headers":   {{"HeaderName": "example-value"}},
  "auth_example":   "string — a complete curl command demonstrating authentication",
  "rate_limits":    "string — rate limit information found in docs, or 'Not specified'",
  "endpoints": [
    {{
      "method":      "GET|POST|PUT|DELETE|PATCH",
      "path":        "/resource/path",
      "description": "clear description of what this endpoint does",
      "params":      "key query/path parameters (comma-separated) or 'None'"
    }}
  ],
  "use_cases":      ["string — common developer use case for this API"],
  "research_notes": "string — notes useful for academic or research use"
}}

CRITICAL RULES:
1. Extract ALL essential endpoints — aim for 15-25 if they exist.
2. Every endpoint object MUST have all 4 fields: method, path, description, params.
3. base_url must be the actual API base URL, not the documentation URL.
4. auth_headers must be a flat key-value dict.
5. Response must be pure, parseable JSON — no comments, no trailing commas.
"""


# ── Validation + Normalisation ────────────────────────────────────────────────

def _normalise_endpoint(raw: dict) -> Endpoint:
    """Ensure an endpoint dict has all required fields with correct types."""
    return {
        "method":      str(raw.get("method", "GET")).upper().strip(),
        "path":        str(raw.get("path", "/")).strip(),
        "description": str(raw.get("description", "—")).strip(),
        "params":      str(raw.get("params", "None")).strip(),
    }


def _validate_spec(data: dict) -> APISpec:
    """
    Validate and normalise the raw dict returned by the LLM.
    Fills missing fields with safe defaults so the UI never crashes.
    """
    auth_headers = data.get("auth_headers", {})
    if not isinstance(auth_headers, dict):
        auth_headers = {}

    raw_endpoints = data.get("endpoints", [])
    if not isinstance(raw_endpoints, list):
        raw_endpoints = []

    return {
        "api_name":       str(data.get("api_name", "Unknown API")).strip(),
        "version":        str(data.get("version",  "N/A")).strip(),
        "base_url":       str(data.get("base_url", "https://api.example.com")).strip(),
        "description":    str(data.get("description", "")).strip(),
        "auth_method":    str(data.get("auth_method", "Unknown")).strip(),
        "auth_headers":   {str(k): str(v) for k, v in auth_headers.items()},
        "auth_example":   str(data.get("auth_example", "")).strip(),
        "rate_limits":    str(data.get("rate_limits", "Not specified")).strip(),
        "endpoints":      [_normalise_endpoint(ep) for ep in raw_endpoints if isinstance(ep, dict)],
        "use_cases":      [str(uc) for uc in data.get("use_cases", []) if isinstance(uc, str)],
        "research_notes": str(data.get("research_notes", "")).strip(),
    }


def _strip_json_fences(text: str) -> str:
    """Strip accidental markdown fences from the LLM response."""
    text = text.strip()
    # Remove ```json ... ``` wrappers
    text = re.sub(r"^```(?:json)?\s*\n?", "", text)
    text = re.sub(r"\n?```$", "", text)
    return text.strip()


# ── Public API ─────────────────────────────────────────────────────────────────

def parse_api_docs(url: str, use_case: str = "") -> APISpec | None:
    """
    Extract a structured APISpec from a documentation URL.

    Args:
        url:      Documentation page URL.
        use_case: Optional developer intent string to filter endpoints.

    Returns:
        A validated APISpec dict, or None if extraction failed.

    Raises:
        RuntimeError: If the Groq API key is not configured.
    """
    # Step 1: Scrape documentation text
    doc_text = fetch_doc_text(url)

    page_context = (
        f"Here is the cleaned text content extracted from the documentation page:\n"
        f"---\n{doc_text}\n---\n\n"
        if doc_text else
        "Note: Could not fetch the documentation page. Use your knowledge of the API at this URL.\n\n"
    )

    use_case_context = (
        f"Developer's specific use case: '{use_case.strip()}'. "
        f"Prioritise extracting endpoints most relevant to this goal.\n\n"
        if use_case.strip() else ""
    )

    # Step 2: Build prompt and call LLM
    user_prompt = _USER_PROMPT_TEMPLATE.format(
        url=url,
        page_context=page_context,
        use_case_context=use_case_context,
    )

    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user",   "content": user_prompt},
    ]

    raw_content = chat_completion(
        messages=messages,
        json_mode=True,
        max_tokens=4096,
        temperature=0.1,
    )

    if not raw_content:
        return None

    # Step 3: Parse JSON
    try:
        cleaned = _strip_json_fences(raw_content)
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return None

    # Step 4: Validate and return
    return _validate_spec(data)

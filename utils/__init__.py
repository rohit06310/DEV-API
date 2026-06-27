"""
utils/__init__.py
──────────────────────────────────────────────────
Public API for the utils package.
Import from here in app.py and components.
"""
from utils.groq_client  import chat_completion, get_client, GROQ_MODEL_PRIMARY
from utils.scraper      import fetch_doc_text, safe_domain
from utils.parser       import parse_api_docs, APISpec
from utils.sdk_generator import generate_sdk, SUPPORTED_LANGUAGES, LANG_EXTENSIONS

__all__ = [
    # Groq client
    "chat_completion",
    "get_client",
    "GROQ_MODEL_PRIMARY",
    # Scraper
    "fetch_doc_text",
    "safe_domain",
    # Parser
    "parse_api_docs",
    "APISpec",
    # SDK generator
    "generate_sdk",
    "SUPPORTED_LANGUAGES",
    "LANG_EXTENSIONS",
]

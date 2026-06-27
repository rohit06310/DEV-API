"""
utils/scraper.py
──────────────────────────────────────────────────
Documentation fetcher and HTML parser.
Strips noise (scripts, styles, nav, footer) and returns
clean, LLM-ready plain text from any documentation URL.
"""
import re
import urllib.parse

import requests
from bs4 import BeautifulSoup

# Tags that add no meaningful textual content
_NOISE_TAGS = [
    "script", "style", "nav", "footer", "header",
    "iframe", "noscript", "aside", "form", "button",
    "head", "svg", "img", "video", "audio",
]

_REQUEST_HEADERS = {
    "User-Agent": "DevFlow/2.0 (API Research Tool; +https://github.com/devflow)",
    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def fetch_doc_text(url: str, max_chars: int = 14000, timeout: int = 8) -> str:
    """
    Fetch an API documentation page and extract its meaningful plain text.

    Strategy:
    1. HTTP GET with a browser-like User-Agent to avoid bot blocks.
    2. Parse HTML with BeautifulSoup (lxml backend for speed).
    3. Remove all noise tags (JS, CSS, nav, footers, etc.).
    4. Prefer <main>, <article>, or role="main" for focused extraction.
    5. Return a whitespace-collapsed plain-text string.

    Args:
        url:       The documentation URL to fetch.
        max_chars: Maximum characters to return (prevents LLM context overflow).
        timeout:   HTTP request timeout in seconds.

    Returns:
        Clean plain text, or an empty string on failure.
    """
    try:
        resp = requests.get(url, headers=_REQUEST_HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
    except requests.RequestException:
        return ""

    try:
        soup = BeautifulSoup(resp.text, "lxml")
    except Exception:
        soup = BeautifulSoup(resp.text, "html.parser")

    # Strip noise tags
    for tag in soup(_NOISE_TAGS):
        tag.decompose()

    # Prefer main content container
    main = (
        soup.find("main")
        or soup.find(attrs={"role": "main"})
        or soup.find("article")
        or soup.find("div", class_=re.compile(r"content|docs|main|body", re.I))
        or soup.body
        or soup
    )

    text = main.get_text(separator=" ", strip=True)
    # Collapse whitespace runs
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


def safe_domain(url: str) -> str:
    """Extract the network location (domain) from a URL safely."""
    try:
        return urllib.parse.urlparse(url).netloc or "api.example.com"
    except Exception:
        return "api.example.com"

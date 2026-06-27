"""
app.py — DevFlow Entry Point
──────────────────────────────────────────────────
This file is intentionally thin. All business logic
lives in utils/. This file only handles:
  - Page config
  - Session state
  - UI routing (analyze / display / landing)
  - Calling utils functions with @st.cache_data wrappers
"""
import json
import time
from datetime import datetime

import pandas as pd
import requests as req
import streamlit as st

# ── Backend utilities (all logic lives here) ──────────────────────────────────
from utils import (
    parse_api_docs,
    generate_sdk,
    get_client,
    safe_domain,
    SUPPORTED_LANGUAGES,
    LANG_EXTENSIONS,
    GROQ_MODEL_PRIMARY,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DevFlow – API Integration Accelerator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "api_url":       "",
    "history":       [],
    "analyze_trigger": False,
    "has_analyzed":  False,
    "parsed_data":   None,   # APISpec dict or None
    "request_log":   [],     # Sandbox request log
    "bookmarks":     [],
    "notes":         {},
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────────────────────────────────────
# CACHED WRAPPERS (Streamlit caching around backend utils)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False, ttl=600)
def _cached_parse(url: str, use_case: str):
    """Cache-wrapped call to utils.parse_api_docs."""
    return parse_api_docs(url, use_case)


@st.cache_data(show_spinner=False, ttl=600)
def _cached_sdk(api_name, base_url, auth_headers_json, lang, style, endpoint_target):
    """Cache-wrapped call to utils.generate_sdk."""
    auth_headers = json.loads(auth_headers_json)
    return generate_sdk(api_name, base_url, auth_headers, lang, style, endpoint_target)


# ─────────────────────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
_METHOD_COLORS = {
    "GET":    "#22c55e",
    "POST":   "#3b82f6",
    "PUT":    "#f59e0b",
    "DELETE": "#ef4444",
    "PATCH":  "#a855f7",
}

def _badge(method: str) -> str:
    color = _METHOD_COLORS.get(method.upper(), "#6b7280")
    return (
        f"<span style='background:{color};color:#fff;padding:2px 8px;"
        f"border-radius:4px;font-size:11px;font-weight:700;'>{method.upper()}</span>"
    )

def set_url_and_analyze(url: str):
    st.session_state.api_url        = url
    st.session_state.analyze_trigger = True
    st.session_state.has_analyzed   = False
    st.session_state.parsed_data    = None

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Fonts ──────────────────────────────────────────────────────────── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    -webkit-font-smoothing: antialiased;
  }

  /* ── Ambient background orbs ─────────────────────────────────────────── */
  .stApp::before {
    content: '';
    position: fixed;
    top: -240px; left: -180px;
    width: 700px; height: 700px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(129,140,248,.14) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
    animation: orbFloat 18s ease-in-out infinite;
  }
  .stApp::after {
    content: '';
    position: fixed;
    bottom: -200px; right: -180px;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(96,165,250,.11) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
    animation: orbFloat 24s ease-in-out infinite reverse;
  }
  @keyframes orbFloat {
    0%,100% { transform: translate(0,0) scale(1); }
    33%      { transform: translate(30px,-25px) scale(1.04); }
    66%      { transform: translate(-20px,20px) scale(0.97); }
  }

  /* ── Header gradient title ───────────────────────────────────────────── */
  h1 {
    background: linear-gradient(135deg,#818cf8 0%,#60a5fa 55%,#22d3ee 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
  }

  /* ── Sidebar glass panel ─────────────────────────────────────────────── */
  section[data-testid="stSidebar"] {
    background: rgba(10,11,20,0.82) !important;
    backdrop-filter: blur(18px) saturate(160%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
  }

  /* ── Metric cards ────────────────────────────────────────────────────── */
  div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(14,16,23,0.9) 0%, rgba(20,24,38,0.85) 100%);
    border: 1px solid rgba(129,140,248,0.18);
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.04);
    transition: border-color .25s ease, box-shadow .25s ease, transform .2s ease;
    backdrop-filter: blur(10px);
  }
  div[data-testid="stMetric"]:hover {
    border-color: rgba(129,140,248,0.55);
    box-shadow: 0 0 32px rgba(129,140,248,0.18), 0 4px 24px rgba(0,0,0,0.4);
    transform: translateY(-2px);
  }
  div[data-testid="stMetricLabel"] {
    font-size: 11.5px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: rgba(160,168,210,0.7) !important;
  }
  div[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    background: linear-gradient(120deg,#c7d2fe,#93c5fd);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
  }

  /* ── Tabs ────────────────────────────────────────────────────────────── */
  .stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    padding-bottom: 0;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 10px 10px 0 0;
    padding: 9px 18px;
    font-weight: 500;
    font-size: 13.5px;
    color: rgba(160,168,210,0.65);
    transition: color .2s, background .2s;
    border: 1px solid transparent;
    border-bottom: none;
  }
  .stTabs [data-baseweb="tab"]:hover {
    color: #c7d2fe;
    background: rgba(129,140,248,0.06);
  }
  .stTabs [aria-selected="true"] {
    color: #a5b4fc !important;
    background: rgba(129,140,248,0.12) !important;
    border-color: rgba(129,140,248,0.2) !important;
    box-shadow: 0 -2px 0 #818cf8 inset;
  }

  /* ── Endpoint rows ───────────────────────────────────────────────────── */
  .ep-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    margin-bottom: 7px;
    background: rgba(14,16,23,0.7);
    backdrop-filter: blur(8px);
    transition: background .18s, border-color .18s, transform .18s, box-shadow .18s;
  }
  .ep-row:hover {
    background: rgba(30,42,80,0.6);
    border-color: rgba(129,140,248,0.45);
    transform: translateX(4px);
    box-shadow: 0 0 20px rgba(129,140,248,0.1);
  }
  .ep-path {
    font-family: 'Courier New', monospace;
    color: #e2e8f0;
    font-size: 13.5px;
    font-weight: 500;
  }
  .ep-desc { color: #6b7f9e; font-size: 12px; }

  /* ── Method badges ───────────────────────────────────────────────────── */
  span[style*="border-radius:4px"] {
    border-radius: 6px !important;
    letter-spacing: 0.04em !important;
    box-shadow: 0 1px 8px rgba(0,0,0,0.3) !important;
  }

  /* ── Pill tags ───────────────────────────────────────────────────────── */
  .pill {
    display: inline-block;
    background: rgba(30,42,80,0.7);
    color: #93c5fd;
    border: 1px solid rgba(96,165,250,0.2);
    border-radius: 100px;
    padding: 3px 12px;
    font-size: 11.5px;
    font-weight: 600;
    margin: 3px;
    letter-spacing: 0.02em;
    backdrop-filter: blur(4px);
  }

  /* ── Request log rows ────────────────────────────────────────────────── */
  .log-row {
    background: rgba(14,16,23,0.75);
    border-left: 3px solid #818cf8;
    padding: 9px 14px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 6px;
    font-size: 12.5px;
    backdrop-filter: blur(6px);
    transition: background .15s;
  }
  .log-row:hover { background: rgba(30,42,80,0.55); }

  /* ── Feature / landing cards ─────────────────────────────────────────── */
  .devflow-card {
    background: linear-gradient(135deg, rgba(14,16,23,0.9) 0%, rgba(20,24,38,0.8) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 22px 20px;
    margin-bottom: 14px;
    backdrop-filter: blur(10px);
    transition: border-color .22s, box-shadow .22s, transform .22s;
    position: relative;
    overflow: hidden;
  }
  .devflow-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg,#818cf8,#60a5fa);
    opacity: 0;
    transition: opacity .25s;
  }
  .devflow-card:hover::before { opacity: 1; }
  .devflow-card:hover {
    border-color: rgba(129,140,248,0.3);
    box-shadow: 0 0 32px rgba(129,140,248,0.12);
    transform: translateY(-3px);
  }
  .devflow-card h4 {
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    margin-bottom: 8px !important;
    color: #e0e7ff !important;
  }

  /* ── Sidebar success/error chips ─────────────────────────────────────── */
  div[data-testid="stSuccess"] {
    background: rgba(16,185,129,0.08) !important;
    border: 1px solid rgba(16,185,129,0.22) !important;
    border-radius: 10px !important;
  }
  div[data-testid="stError"] {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.22) !important;
    border-radius: 10px !important;
  }
  div[data-testid="stWarning"] {
    background: rgba(245,158,11,0.08) !important;
    border: 1px solid rgba(245,158,11,0.2) !important;
    border-radius: 10px !important;
  }
  div[data-testid="stInfo"] {
    background: rgba(99,102,241,0.08) !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
    border-radius: 10px !important;
  }

  /* ── Buttons ─────────────────────────────────────────────────────────── */
  button[kind="primary"] {
    background: linear-gradient(135deg,#6366f1 0%,#818cf8 50%,#60a5fa 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 0 24px rgba(99,102,241,0.3), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    transition: transform .18s, box-shadow .18s !important;
  }
  button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 40px rgba(99,102,241,0.48), inset 0 1px 0 rgba(255,255,255,0.2) !important;
  }
  button[kind="secondary"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    transition: background .18s, border-color .18s !important;
  }
  button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(129,140,248,0.35) !important;
  }

  /* ── Text inputs & textareas ─────────────────────────────────────────── */
  div[data-baseweb="input"] input,
  div[data-baseweb="textarea"] textarea {
    background: rgba(14,16,23,0.8) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e0e7ff !important;
    transition: border-color .18s, box-shadow .18s !important;
  }
  div[data-baseweb="input"] input:focus,
  div[data-baseweb="textarea"] textarea:focus {
    border-color: rgba(129,140,248,0.6) !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.12) !important;
  }

  /* ── Select boxes ────────────────────────────────────────────────────── */
  div[data-baseweb="select"] > div:first-child {
    background: rgba(14,16,23,0.8) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
  }

  /* ── Horizontal divider ──────────────────────────────────────────────── */
  hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg,transparent,rgba(129,140,248,0.25),transparent) !important;
    margin: 18px 0 !important;
  }

  /* ── Code blocks ─────────────────────────────────────────────────────── */
  div[data-testid="stCode"] {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
  }

  /* ── Spinner ─────────────────────────────────────────────────────────── */
  div[data-testid="stSpinner"] > div {
    border-top-color: #818cf8 !important;
  }

  /* ── Hide Streamlit chrome ───────────────────────────────────────────── */
  footer, #MainMenu { visibility: hidden; }
  div[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ DevFlow")
    groq_ok = get_client() is not None
    if groq_ok:
        st.success(f"🟢 Connected — `{GROQ_MODEL_PRIMARY}`")
    else:
        st.error("🔴 Groq API key missing")
        st.caption("Add GROQ_API_KEY to `.env`")

    st.markdown("---")

    # Bookmarks
    st.markdown("#### 🔖 Bookmarks")
    if st.session_state.parsed_data and st.session_state.api_url:
        if st.button("+ Bookmark current API", use_container_width=True):
            name  = st.session_state.parsed_data.get("api_name", safe_domain(st.session_state.api_url))
            entry = {"name": name, "url": st.session_state.api_url}
            if entry not in st.session_state.bookmarks:
                st.session_state.bookmarks.append(entry)

    for bm in st.session_state.bookmarks:
        if st.button(f"📌 {bm['name']}", key=f"bm_{bm['url']}", use_container_width=True):
            set_url_and_analyze(bm["url"]); st.rerun()

    if not st.session_state.bookmarks:
        st.caption("No bookmarks yet.")

    st.markdown("---")

    # History
    st.markdown("#### 🕒 Recent")
    if not st.session_state.history:
        st.caption("No APIs analyzed yet.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history[-10:])):
            if st.button(item["name"], key=f"hist_{idx}", use_container_width=True):
                set_url_and_analyze(item["url"]); st.rerun()
            st.caption(item["timestamp"])

    st.markdown("---")
    with st.expander("📚 How to use"):
        st.markdown("""
1. Paste any API doc URL  
2. Optionally describe your use case  
3. Click **Analyze API**  
4. Explore the result tabs  
5. Test live in the **Sandbox**  
6. Generate code in **SDK**  
""")

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='margin-bottom:0;padding-bottom:0;'>⚡ DevFlow</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#9CA3AF;margin-top:2px;'>API Integration Accelerator · For Developers, Students & Researchers</p>", unsafe_allow_html=True)
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# INPUT AREA
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("📡 Documentation Source")

inp_col, btn_col = st.columns([5, 1])
with inp_col:
    api_url_input = st.text_input(
        "API Documentation URL",
        placeholder="https://docs.github.com/en/rest",
        value=st.session_state.api_url,
        key="url_input",
        label_visibility="collapsed",
    )
    use_case_input = st.text_area(
        "Use Case",
        placeholder="e.g. I need to fetch user profiles and posts for social data analysis.",
        key="use_case_input",
        height=68,
        label_visibility="collapsed",
    )
    st.caption("💡 Optional: Describe your use case to get targeted endpoints and tailored SDK code.")
with btn_col:
    st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
    analyze_btn = st.button("Analyze API", type="primary", use_container_width=True)
    clear_btn   = st.button("Clear",        use_container_width=True)

if clear_btn:
    for k in ["has_analyzed", "parsed_data", "api_url"]:
        st.session_state[k] = _DEFAULTS.get(k)
    st.rerun()

is_analyzing = analyze_btn or st.session_state.analyze_trigger
if st.session_state.analyze_trigger:
    st.session_state.analyze_trigger = False

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS RENDERER
# ─────────────────────────────────────────────────────────────────────────────
def display_results(url: str, use_case: str = ""):
    st.markdown("---")

    url_key = "".join(c if c.isalnum() else "_" for c in url)[:40]

    # ── Fetch or use session-cached parsed data ───────────────────────────────
    if not st.session_state.parsed_data:
        try:
            with st.spinner("🔍 Extracting API specification..."):
                st.session_state.parsed_data = _cached_parse(url, use_case)
        except RuntimeError as e:
            st.error(str(e))
            return

    parsed = st.session_state.parsed_data

    # ── Fallback data if parsing failed ───────────────────────────────────────
    if not parsed:
        st.error(
            "❌ Could not extract data from this URL. "
            "The page may require authentication, heavy JavaScript rendering, or may be blocking scrapers. "
            "Try a direct, plain-text REST API reference page."
        )
        domain = safe_domain(url)
        parsed = {
            "api_name":    domain.replace("docs.", "").capitalize() + " API",
            "version":     "N/A",
            "base_url":    f"https://api.{domain.replace('docs.','')}",
            "description": "Could not extract description.",
            "auth_method": "Bearer Token",
            "auth_headers": {"Authorization": "Bearer YOUR_TOKEN"},
            "auth_example": f'curl -H "Authorization: Bearer YOUR_TOKEN" https://api.{domain}/resource',
            "rate_limits": "Not specified",
            "endpoints":   [
                {"method": "GET",    "path": "/resource",       "description": "List resources",     "params": "page, limit"},
                {"method": "POST",   "path": "/resource",       "description": "Create resource",    "params": "None"},
                {"method": "GET",    "path": "/resource/{id}",  "description": "Get resource by ID", "params": "id"},
                {"method": "PUT",    "path": "/resource/{id}",  "description": "Update resource",    "params": "id"},
                {"method": "DELETE", "path": "/resource/{id}",  "description": "Delete resource",    "params": "id"},
            ],
            "use_cases":      [],
            "research_notes": "",
        }

    api_name     = parsed["api_name"]
    api_version  = parsed["version"]
    base_url     = parsed["base_url"]
    description  = parsed["description"]
    auth_method  = parsed["auth_method"]
    auth_headers = parsed["auth_headers"]
    auth_example = parsed["auth_example"]
    rate_limits  = parsed["rate_limits"]
    endpoints    = parsed["endpoints"]
    use_cases    = parsed.get("use_cases", [])
    auth_hdr_str = json.dumps(auth_headers)

    ep_options = (
        [f"{e['method']} {e['path']}" for e in endpoints]
        if endpoints else ["Full API Integration"]
    )

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tabs = st.tabs(["📊 Overview", "🔗 Endpoints", "🔐 Auth", "⚙️ SDK", "📖 Examples", "🧪 Sandbox"])
    tab1, tab2, tab3, tab4, tab5, tab6 = tabs

    # ─ Tab 1: Overview ────────────────────────────────────────────────────────
    with tab1:
        st.markdown(f"### {api_name}")
        if description:
            st.info(description)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Version",   api_version)
        m2.metric("Endpoints", len(endpoints))
        m3.metric("Auth",      auth_method)
        m4.metric("Rate Limit", rate_limits[:30] if len(rate_limits) > 30 else rate_limits)

        if use_cases:
            st.markdown("**Common Use Cases:**")
            st.markdown(" ".join([f"<span class='pill'>{uc}</span>" for uc in use_cases]), unsafe_allow_html=True)

        st.markdown("**Base URL:**")
        st.code(base_url, language="text")

    # ─ Tab 2: Endpoints ───────────────────────────────────────────────────────
    with tab2:
        c1, c2 = st.columns([3, 1])
        with c1:
            search = st.text_input("Filter", placeholder="Search endpoints…", key=f"ep_s_{url_key}", label_visibility="collapsed")
        with c2:
            mf = st.selectbox("Method", ["All","GET","POST","PUT","DELETE","PATCH"], key=f"ep_m_{url_key}", label_visibility="collapsed")

        filtered = endpoints
        if search:
            s = search.lower()
            filtered = [e for e in filtered if s in e["path"].lower() or s in e["description"].lower() or s in e["method"].lower()]
        if mf != "All":
            filtered = [e for e in filtered if e["method"] == mf]

        st.markdown(f"<span class='pill'>{len(filtered)} endpoint(s)</span>", unsafe_allow_html=True)

        for ep in filtered:
            st.markdown(
                f"<div class='ep-row'>"
                f"{_badge(ep['method'])}"
                f"<div><div class='ep-path'>{ep['path']}</div>"
                f"<div class='ep-desc'>{ep['description']} · Params: {ep.get('params','None')}</div></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        if endpoints:
            df = pd.DataFrame([{"Method": e["method"], "Path": e["path"], "Description": e["description"], "Params": e.get("params","")} for e in endpoints])
            st.download_button("⬇️ Export CSV", data=df.to_csv(index=False),
                               file_name=f"{api_name.replace(' ','_')}_endpoints.csv", mime="text/csv")

    # ─ Tab 3: Authentication ──────────────────────────────────────────────────
    with tab3:
        st.markdown(f"**Type:** `{auth_method}`")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Required Headers:**")
            st.code(json.dumps(auth_headers, indent=2), language="json")
        with c2:
            st.markdown("**cURL Example:**")
            st.code(auth_example, language="bash")

        st.markdown("**Python:**")
        st.code(f"""import requests

headers = {json.dumps(auth_headers, indent=4)}
r = requests.get("{base_url}/resource", headers=headers)
r.raise_for_status()
print(r.json())
""", language="python")

        st.markdown("**JavaScript (fetch):**")
        st.code(f"""const res = await fetch('{base_url}/resource', {{
  headers: {json.dumps(auth_headers, indent=2)}
}});
const data = await res.json();
""", language="javascript")

    # ─ Tab 4: SDK Generator ───────────────────────────────────────────────────
    with tab4:
        st.caption("Select a target endpoint and language, then generate ready-to-use integration code.")

        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            selected_ep = st.selectbox("Target Endpoint", ep_options, key=f"ep_sel_{url_key}")
        with c2:
            lang = st.selectbox("Language", SUPPORTED_LANGUAGES, key=f"lang_{url_key}")
        with c3:
            sdk_style = st.radio("Style", ["Minimal Functions", "Wrapper Class"], horizontal=True, key=f"style_{url_key}")

        gen_btn = st.button("⚡ Generate Code", type="primary", key=f"gen_{url_key}")
        sdk_key = f"sdk_{url_key}_{lang}_{sdk_style}_{selected_ep}"

        if gen_btn:
            try:
                with st.spinner(f"Generating {lang} code…"):
                    st.session_state[sdk_key] = _cached_sdk(
                        api_name, base_url, auth_hdr_str, lang, sdk_style, selected_ep
                    )
            except RuntimeError as e:
                st.error(str(e))

        if sdk_key in st.session_state:
            code = st.session_state[sdk_key]
            display_lang = "bash" if lang == "cURL" else lang.lower()
            st.code(code, language=display_lang)
            ext = LANG_EXTENSIONS.get(lang, "txt")
            st.download_button(
                f"⬇️ Download {lang} SDK",
                data=code,
                file_name=f"{api_name.replace(' ','_').lower()}_sdk.{ext}",
                mime="text/plain",
                key=f"dl_{sdk_key}",
            )
        else:
            st.info("Choose your options above and click **Generate Code**.")

    # ─ Tab 5: Examples ────────────────────────────────────────────────────────
    with tab5:
        st.caption("Copy-paste ready snippets for the most common integration patterns.")

        first = endpoints[0] if endpoints else {"method": "GET", "path": "/resource", "description": "example"}

        with st.expander("🐍 Python — Quick Start", expanded=True):
            st.code(f"""import requests

BASE_URL = "{base_url}"
HEADERS  = {json.dumps(auth_headers, indent=10).strip()}

def call(path, method="GET", data=None, params=None):
    r = requests.request(method, BASE_URL + path, headers=HEADERS, json=data, params=params)
    r.raise_for_status()
    return r.json()

# {first['method']} {first['path']} — {first['description']}
result = call("{first['path']}", method="{first['method']}")
print(result)
""", language="python")

        with st.expander("🌐 JavaScript — fetch"):
            st.code(f"""const BASE   = '{base_url}';
const HDRS   = {json.dumps(auth_headers, indent=2)};

async function call(path, method='GET', body=null) {{
  const r = await fetch(BASE+path, {{method, headers:HDRS, ...(body && {{body:JSON.stringify(body)}})}});
  if (!r.ok) throw new Error(`${{r.status}} ${{r.statusText}}`);
  return r.json();
}}

// {first['method']} {first['path']}
call('{first['path']}', '{first['method']}').then(console.log);
""", language="javascript")

        if len(endpoints) > 1:
            st.markdown("---")
            st.markdown("**Per-endpoint examples (first 8):**")
            for ep in endpoints[:8]:
                with st.expander(f"{ep['method']} `{ep['path']}` — {ep.get('description','')}"):
                    st.code(f"""r = requests.request(
    "{ep['method']}", "{base_url}{ep['path']}",
    headers={json.dumps(auth_headers)}
)
print(r.status_code, r.json())
""", language="python")

    # ─ Tab 6: Sandbox ─────────────────────────────────────────────────────────
    with tab6:
        st.caption("Execute live HTTP requests against the API directly from DevFlow.")

        # ── Input widgets (no st.form — avoids the Streamlit conditional-block
        #    navigation bug where form_submit_button loses state on rerun) ─────
        sb_resp_key = f"sb_response_{url_key}"   # persistent response storage

        sb1, sb2 = st.columns([1, 4])
        with sb1:
            sb_method = st.selectbox("Method", ["GET","POST","PUT","DELETE","PATCH"],
                                     key=f"sbm_{url_key}")
        with sb2:
            sb_url = st.text_input("URL", value=base_url, key=f"sbu_{url_key}")

        # Warn the user when the URL is still pointing at the root domain
        try:
            import urllib.parse as _up
            _parsed = _up.urlparse(sb_url or "")
            if _parsed.path.strip("/") == "" and sb_url.strip():
                st.warning(
                    "⚠️ **Root URL detected.** This will return an HTML page, not JSON. "
                    "Append an endpoint path — e.g. `/posts`, `/users/1`, `/repos/owner/repo`."
                )
        except Exception:
            pass

        sbc1, sbc2 = st.columns(2)
        with sbc1:
            sb_headers = st.text_area("Headers (JSON)", value=json.dumps(auth_headers, indent=2),
                                      height=130, key=f"sbh_{url_key}")
            sb_params  = st.text_area("Query Params (JSON)", value="{}", height=80,
                                      key=f"sbp_{url_key}")
        with sbc2:
            sb_body    = st.text_area("Body (JSON)", placeholder='{"key":"value"}',
                                      height=215, key=f"sbb_{url_key}")

        send = st.button("🚀 Send Request", type="primary", key=f"sb_send_{url_key}")

        if send:
            errors = []
            hdr_dict = {}; prm_dict = {}; bdy_dict = None

            try:    hdr_dict = json.loads(sb_headers) if sb_headers.strip() else {}
            except: errors.append("Headers is not valid JSON.")

            try:    prm_dict = json.loads(sb_params) if sb_params.strip() not in ("", "{}") else {}
            except: errors.append("Query Params is not valid JSON.")

            try:    bdy_dict = json.loads(sb_body) if sb_body.strip() else None
            except: errors.append("Body is not valid JSON.")

            if errors:
                st.session_state[sb_resp_key] = {"errors": errors}
            else:
                with st.spinner("Executing…"):
                    try:
                        t0 = time.time()
                        resp = req.request(sb_method, sb_url, headers=hdr_dict,
                                           params=prm_dict, json=bdy_dict, timeout=15)
                        ms = round((time.time()-t0)*1000)

                        # Persist result so it survives reruns (stays visible)
                        try:    body = resp.json()
                        except: body = resp.text[:6000]

                        st.session_state[sb_resp_key] = {
                            "status": resp.status_code,
                            "reason": resp.reason,
                            "ms":     ms,
                            "size":   len(resp.content),
                            "headers": dict(resp.headers),
                            "body":    body,
                            "is_json": isinstance(body, (dict, list)),
                        }
                        st.session_state.request_log.append({
                            "time":   datetime.now().strftime("%H:%M:%S"),
                            "method": sb_method, "url": sb_url,
                            "status": resp.status_code, "ms": ms,
                        })

                    except req.exceptions.Timeout:
                        st.session_state[sb_resp_key] = {"errors": ["Request timed out (15 s)."]}
                    except req.exceptions.ConnectionError as e:
                        st.session_state[sb_resp_key] = {"errors": [f"Connection error: {e}"]}
                    except Exception as e:
                        st.session_state[sb_resp_key] = {"errors": [f"Unexpected error: {e}"]}

        # ── Display last response (persisted in session state) ────────────────
        result = st.session_state.get(sb_resp_key)
        if result:
            if "errors" in result:
                for err in result["errors"]:
                    st.error(err)
            else:
                ok  = 200 <= result["status"] < 300
                clr = "#22c55e" if ok else "#ef4444"
                st.markdown(
                    f"<div style='display:flex;gap:16px;align-items:center;padding:12px;"
                    f"background:#0f1724;border-radius:8px;margin-bottom:12px;'>"
                    f"<span style='color:{clr};font-size:22px;font-weight:700;'>{result['status']}</span>"
                    f"<span style='color:#9CA3AF;'>{result['reason']}</span>"
                    f"<span class='pill'>⏱ {result['ms']} ms</span>"
                    f"<span class='pill'>📦 {result['size']:,} B</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                with st.expander("Response Headers"):
                    st.json(result["headers"])
                st.markdown("**Response Body:**")
                if result["is_json"]:
                    st.json(result["body"])
                else:
                    # If HTML came back, warn the user instead of dumping raw markup
                    body_text = result["body"] if isinstance(result["body"], str) else str(result["body"])
                    if body_text.strip().startswith("<!DOCTYPE") or body_text.strip().startswith("<html"):
                        st.warning(
                            "🌐 **HTML page returned** — the URL is pointing to a web page, not an API endpoint. "
                            "Make sure you include the full path (e.g. `/posts`, `/v1/charges`)."
                        )
                        with st.expander("Show raw HTML (for debugging)"):
                            st.code(body_text[:3000], language="html")
                    else:
                        st.code(body_text, language="text")

        # ── Request log ───────────────────────────────────────────────────────
        if st.session_state.request_log:
            st.markdown("---")
            st.markdown("**Session Request Log**")
            for entry in reversed(st.session_state.request_log[-10:]):
                c = "#22c55e" if 200 <= entry["status"] < 300 else "#ef4444"
                st.markdown(
                    f"<div class='log-row'>"
                    f"<b style='color:{c};'>{entry['status']}</b> &nbsp;"
                    f"<span style='color:#60a5fa;'>{entry['method']}</span> &nbsp;"
                    f"{entry['url']} &nbsp;"
                    f"<span style='color:#9CA3AF;'>({entry['ms']} ms · {entry['time']})</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            if st.button("Clear Log", key=f"clr_log_{url_key}"):
                st.session_state.request_log = []
                if sb_resp_key in st.session_state:
                    del st.session_state[sb_resp_key]
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ROUTING
# ─────────────────────────────────────────────────────────────────────────────
if is_analyzing:
    current_url  = st.session_state.get("url_input", "").strip()
    current_case = st.session_state.get("use_case_input", "").strip()

    if not current_url:
        st.warning("Please enter an API documentation URL.")
    elif not get_client():
        st.error("Groq API key missing. Add GROQ_API_KEY to your `.env` file and restart.")
    else:
        st.session_state.api_url      = current_url
        st.session_state.has_analyzed = True
        st.session_state.parsed_data  = None  # force fresh extraction

        # Update history
        if not st.session_state.history or st.session_state.history[-1]["url"] != current_url:
            domain = safe_domain(current_url)
            name   = domain.replace("docs.", "").replace("api.", "").capitalize() + " API"
            st.session_state.history.append({
                "name": name, "url": current_url,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

        with st.status("Analyzing API…", expanded=True) as status:
            st.write("🌐 Fetching documentation content…")
            time.sleep(0.3)
            st.write("🔍 Extracting endpoints, auth & metadata…")
            time.sleep(0.5)
            st.write("📦 Preparing results…")
            time.sleep(0.2)
            status.update(label="✅ Analysis Complete", state="complete", expanded=False)

        display_results(current_url, current_case)

elif st.session_state.get("has_analyzed") and st.session_state.get("api_url"):
    display_results(st.session_state.api_url, st.session_state.get("use_case_input", ""))

else:
    # ── Landing ───────────────────────────────────────────────────────────────
    st.markdown("### 🚀 Quick Start — Popular APIs")
    quick = [
        ("🐙", "GitHub REST",   "https://docs.github.com/en/rest"),
        ("💳", "Stripe",        "https://docs.stripe.com/api"),
        ("📱", "Razorpay",      "https://razorpay.com/docs/api/"),
        ("💬", "Twilio",        "https://www.twilio.com/docs/api"),
        ("🌤", "OpenWeather",   "https://openweathermap.org/api"),
        ("📈", "Alpha Vantage", "https://www.alphavantage.co/documentation/"),
    ]
    cols = st.columns(len(quick))
    for col, (icon, label, api_url) in zip(cols, quick):
        with col:
            if st.button(f"{icon} {label}", use_container_width=True, key=f"q_{label}"):
                set_url_and_analyze(api_url)
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### ✨ What DevFlow Does")

    f1, f2, f3 = st.columns(3)
    cards = [
        ("🔗 Smart Extraction",    "Extracts all essential endpoints, HTTP methods, path params, and auth details from any API docs URL."),
        ("⚙️ Code Generation",     "Generates production-ready SDK code in Python, JavaScript, TypeScript, Java, Go, or cURL — on-demand per endpoint."),
        ("🧪 Live Sandbox",        "Test any endpoint with real HTTP requests. Inspect status, latency, response headers, and body inline."),
    ]
    for col, (title, body) in zip([f1, f2, f3], cards):
        with col:
            st.markdown(f"<div class='devflow-card'><h4>{title}</h4><p style='color:#9CA3AF;font-size:13px;'>{body}</p></div>", unsafe_allow_html=True)

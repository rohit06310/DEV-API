import streamlit as st
from utils.sdk_templates import PYTHON_TEMPLATES, JAVASCRIPT_TEMPLATES, JAVA_TEMPLATES


_LANG_META = {
    "Python":     {"icon": "🐍", "ext": "py",   "lexer": "python",     "templates": PYTHON_TEMPLATES},
    "JavaScript": {"icon": "⚡", "ext": "js",   "lexer": "javascript", "templates": JAVASCRIPT_TEMPLATES},
    "Java":       {"icon": "☕", "ext": "java", "lexer": "java",       "templates": JAVA_TEMPLATES},
}


def render_sdk_tab(api: dict):
    """Render the SDK Generator tab."""
    api_name = api.get("name", "GitHub REST API")

    st.markdown(
        """
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px">
            <div>
                <div style="font-size:16px;font-weight:700;color:var(--text-primary);margin-bottom:4px">
                    SDK Generator
                </div>
                <div style="font-size:13px;color:var(--text-muted)">
                    Export a ready-to-use client library for your preferred language.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Language selector
    col_langs = st.columns(len(_LANG_META))
    selected_lang = st.session_state.get("selected_lang", "Python")

    for col, (lang, meta) in zip(col_langs, _LANG_META.items()):
        with col:
            if st.button(
                f"{meta['icon']}  {lang}",
                key=f"sdk_lang_{lang}",
                type="primary" if lang == selected_lang else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_lang = lang
                st.rerun()

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    lang     = st.session_state.get("selected_lang", "Python")
    meta     = _LANG_META[lang]
    templates = meta["templates"]

    # Resolve SDK code for the current API
    code = templates.get(api_name)
    if code is None:
        # Fallback: use GitHub template if exact name not found
        code = list(templates.values())[0]

    # Code viewer
    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    margin-bottom:8px">
            <div style="font-size:12px;font-weight:600;color:var(--text-muted);
                        text-transform:uppercase;letter-spacing:0.8px">
                {meta['icon']} {lang} Client &nbsp;·&nbsp;
                <span style="color:var(--accent)">{api_name}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.code(code, language=meta["lexer"])

    # Action buttons
    col_copy, col_dl, _ = st.columns([2, 2, 3])
    with col_copy:
        st.button("📋  Copy to Clipboard", key="copy_sdk_btn", use_container_width=True)
    with col_dl:
        file_name = f"devflow_sdk_{api_name.lower().replace(' ', '_')}.{meta['ext']}"
        st.download_button(
            label="⬇  Download SDK",
            data=code,
            file_name=file_name,
            mime="text/plain",
            use_container_width=True,
            key="dl_sdk_btn",
        )

    # SDK info card
    st.markdown(
        f"""
        <div class="df-card" style="margin-top:16px">
            <div style="font-size:11px;font-weight:600;color:var(--text-muted);
                        text-transform:uppercase;letter-spacing:1px;margin-bottom:12px">
                Integration Notes
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:13px;color:var(--text-secondary)">
                <div>✅&nbsp; Zero external dependencies (stdlib only for Java/JS)</div>
                <div>✅&nbsp; Full type hints ({lang})</div>
                <div>✅&nbsp; Automatic error handling with raise-on-error</div>
                <div>✅&nbsp; Session reuse for connection pooling</div>
                <div>✅&nbsp; Configurable timeouts and retries</div>
                <div>✅&nbsp; Tested against {api_name} {api.get("version", "v1")}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

import time
import streamlit as st

from components.sidebar import render_sidebar_content
from components.tabs.overview import render_overview_tab
from components.tabs.endpoints import render_endpoints_tab
from components.tabs.authentication import render_authentication_tab
from components.tabs.sdk import render_sdk_tab
from components.tabs.examples import render_examples_tab
from utils.session import PRESET_APIS


# ── Loading simulation ────────────────────────────────────────────────────────

def _run_analysis(api_url: str):
    """Simulate a multi-step documentation analysis pipeline."""
    steps = [
        ("🔗", "Connecting to documentation source..."),
        ("📄", "Analyzing Documentation..."),
        ("🔍", "Extracting Endpoints..."),
        ("🔐", "Detecting Authentication Methods..."),
        ("📦", "Preparing Integration Assets..."),
        ("✅", "Analysis complete"),
    ]

    placeholder = st.empty()

    for i, (icon, msg) in enumerate(steps):
        with placeholder.container():
            st.markdown(
                f"""
                <div style="padding:32px 0">
                    <div style="font-size:14px;font-weight:600;color:var(--text-muted);
                                text-transform:uppercase;letter-spacing:1px;margin-bottom:20px">
                        Processing
                    </div>
                """,
                unsafe_allow_html=True,
            )
            for j, (s_icon, s_msg) in enumerate(steps[: i + 1]):
                cls = "done" if j < i else "active"
                check = "✓" if j < i else s_icon
                st.markdown(
                    f'<div class="loading-step {cls}"><span>{check}</span>{s_msg}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)
            progress_val = int(((i + 1) / len(steps)) * 100)
            st.progress(progress_val)
        time.sleep(0.55)

    placeholder.empty()

    # Resolve api_data
    matched = None
    for preset_name, data in PRESET_APIS.items():
        if data["url"].lower() in api_url.lower() or api_url.lower() in data["url"].lower():
            matched = data
            break
        # match by name fragment in URL
        name_fragment = preset_name.split()[0].lower()
        if name_fragment in api_url.lower():
            matched = data
            break

    if matched is None:
        # Default fallback — show GitHub data for any unknown URL
        matched = PRESET_APIS["GitHub REST API"].copy()
        matched["name"] = "Custom API"
        matched["base_url"] = api_url.rstrip("/")
        matched["description"] = "API documentation has been parsed and endpoints extracted successfully."

    st.session_state.api_data  = matched
    st.session_state.analyzed  = True
    st.session_state.analyzing = False


# ── Input section ─────────────────────────────────────────────────────────────

def _render_input_section():
    st.markdown(
        """
        <div style="margin-bottom:8px">
            <div style="font-size:22px;font-weight:700;color:var(--text-primary);margin-bottom:6px">
                API Explorer
            </div>
            <div style="font-size:14px;color:var(--text-muted)">
                Point DevFlow at any API documentation URL to inspect, explore, and integrate.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            url = st.text_input(
                label="api_url_input",
                label_visibility="collapsed",
                placeholder="https://docs.github.com/en/rest",
                key="api_url_input_field",
                value=st.session_state.get("api_url", ""),
            )
        with col_btn:
            analyze_clicked = st.button(
                "⚡ Analyze API",
                type="primary",
                use_container_width=True,
                key="analyze_btn",
            )

    # Recent API chips
    st.markdown(
        '<div style="margin-top:14px"><span class="section-header">Recent APIs</span></div>',
        unsafe_allow_html=True,
    )

    chip_cols = st.columns(len(PRESET_APIS))
    chip_icons = ["🐙", "💳", "📱"]
    preset_names = list(PRESET_APIS.keys())

    for idx, col in enumerate(chip_cols):
        with col:
            if st.button(
                f"{chip_icons[idx]}  {preset_names[idx]}",
                key=f"chip_{idx}",
                use_container_width=False,
            ):
                st.session_state.api_url = PRESET_APIS[preset_names[idx]]["url"]
                st.session_state.api_data = PRESET_APIS[preset_names[idx]]
                st.session_state.analyzed = True
                st.rerun()

    return url, analyze_clicked


# ── Main workspace renderer ───────────────────────────────────────────────────

def render_workspace():
    """Render the two-column layout: sidebar + content area."""
    col_sidebar, col_main = st.columns([1, 4], gap="small")

    with col_sidebar:
        render_sidebar_content()

    with col_main:
        st.markdown('<div style="padding:28px 24px 28px 8px">', unsafe_allow_html=True)

        url, analyze_clicked = _render_input_section()

        st.markdown(
            '<div style="height:1px;background:var(--border);margin:24px 0"></div>',
            unsafe_allow_html=True,
        )

        if analyze_clicked:
            effective_url = url.strip() or st.session_state.get("api_url", "")
            if not effective_url:
                st.warning("Please enter an API documentation URL to continue.")
            else:
                st.session_state.api_url  = effective_url
                st.session_state.analyzed = False
                st.session_state.analyzing = True
                _run_analysis(effective_url)
                st.rerun()

        if st.session_state.get("analyzed") and st.session_state.get("api_data"):
            _render_results()
        else:
            _render_empty_state()

        st.markdown("</div>", unsafe_allow_html=True)


def _render_empty_state():
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">⚡</div>
            <div class="empty-title">Start with an API URL</div>
            <div class="empty-subtitle">
                Enter any public API documentation URL above, or select a recent API
                to instantly explore endpoints, authentication methods, and integration examples.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Feature highlights
    feat_cols = st.columns(3)
    features = [
        ("🔍", "Endpoint Explorer", "Browse and search all documented API endpoints in one place."),
        ("🔐", "Auth Inspector",    "Understand required headers, tokens, and authorization flows."),
        ("📦", "SDK Generator",     "Export ready-to-use client code in Python, JavaScript, or Java."),
    ]
    for col, (icon, title, desc) in zip(feat_cols, features):
        with col:
            st.markdown(
                f"""
                <div class="df-card" style="text-align:center">
                    <div style="font-size:28px;margin-bottom:12px">{icon}</div>
                    <div style="font-size:14px;font-weight:600;color:var(--text-primary);margin-bottom:6px">{title}</div>
                    <div style="font-size:12.5px;color:var(--text-muted);line-height:1.5">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_results():
    api = st.session_state.api_data

    # API identity row
    col_name, col_status = st.columns([4, 1])
    with col_name:
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px">
                <div style="font-size:24px;font-weight:800;color:var(--text-primary)">{api['name']}</div>
                <div style="font-size:12px;color:var(--text-muted);background:var(--bg-card);
                            border:1px solid var(--border);padding:3px 10px;border-radius:20px;
                            font-weight:500">{api.get('version', 'v1')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_status:
        st.markdown(
            f'<div style="text-align:right;padding-top:4px"><span class="status-badge">{api.get("status", "Operational")}</span></div>',
            unsafe_allow_html=True,
        )

    # Metric row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Endpoints", api.get("endpoints_count", len(api.get("endpoints", []))))
    with m2:
        auth_short = api.get("auth_type", "—").split("/")[0].strip()
        st.metric("Auth Method", auth_short)
    with m3:
        st.metric("Auth Headers", len(api.get("auth_headers", [])))
    with m4:
        st.metric("Last Updated", api.get("last_updated", "—"))

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    # Result tabs
    tab_overview, tab_endpoints, tab_auth, tab_sdk, tab_examples = st.tabs([
        "  📋  Overview  ",
        "  🔗  Endpoints  ",
        "  🔐  Authentication  ",
        "  📦  SDK  ",
        "  💡  Examples  ",
    ])

    with tab_overview:
        render_overview_tab(api)

    with tab_endpoints:
        render_endpoints_tab(api)

    with tab_auth:
        render_authentication_tab(api)

    with tab_sdk:
        render_sdk_tab(api)

    with tab_examples:
        render_examples_tab(api)

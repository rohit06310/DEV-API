import streamlit as st
from utils.session import PRESET_APIS


def render_sidebar():
    """Render the left sidebar using Streamlit columns (no native sidebar)."""
    # The sidebar is embedded inside the workspace via a two-column layout.
    # This module exists for logical separation; actual rendering is in workspace.py.
    pass


def render_sidebar_content():
    """Render the sidebar HTML inside a column."""
    api_data = st.session_state.get("api_data")
    analyzed = st.session_state.get("analyzed", False)

    recent_label = "RECENT APIS"
    workspace_label = "WORKSPACE"

    sidebar_html = f"""
    <div class="devflow-sidebar" style="min-height:calc(100vh - 58px)">
        <div class="sidebar-section">
            <div class="sidebar-label">{workspace_label}</div>
            <div class="sidebar-item active">
                <span class="sidebar-icon">🔍</span> API Explorer
            </div>
            <div class="sidebar-item">
                <span class="sidebar-icon">📦</span> Collections
            </div>
            <div class="sidebar-item">
                <span class="sidebar-icon">⚙️</span> Environments
            </div>
            <div class="sidebar-item">
                <span class="sidebar-icon">📜</span> History
            </div>
        </div>

        <div style="height:1px;background:var(--border);margin:0 16px 20px;"></div>

        <div class="sidebar-section">
            <div class="sidebar-label">{recent_label}</div>
    """

    for name in PRESET_APIS:
        icon = "🐙" if "GitHub" in name else ("💳" if "Stripe" in name else "📱")
        active_cls = "active" if (analyzed and api_data and api_data.get("name") == name) else ""
        sidebar_html += f"""
            <div class="sidebar-item {active_cls}">
                <span class="sidebar-icon">{icon}</span> {name}
            </div>
        """

    sidebar_html += """
        </div>

        <div style="height:1px;background:var(--border);margin:0 16px 20px;"></div>

        <div class="sidebar-section">
            <div class="sidebar-label">TOOLS</div>
            <div class="sidebar-item">
                <span class="sidebar-icon">🔒</span> Auth Manager
            </div>
            <div class="sidebar-item">
                <span class="sidebar-icon">📊</span> Analytics
            </div>
            <div class="sidebar-item">
                <span class="sidebar-icon">🔗</span> Webhooks
            </div>
        </div>
    </div>
    """
    st.markdown(sidebar_html, unsafe_allow_html=True)

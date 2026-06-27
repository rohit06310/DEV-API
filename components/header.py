import streamlit as st


def render_header():
    """Render the top navigation bar."""
    st.markdown(
        """
        <div class="devflow-navbar">
            <div class="devflow-logo">
                <div class="devflow-logo-icon">⚡</div>
                <div>
                    <div class="devflow-logo-text">Dev<span>Flow</span></div>
                    <div class="devflow-tagline">Accelerate API Integration</div>
                </div>
            </div>
            <div class="nav-pills">
                <span class="nav-pill active">Workspace</span>
                <span class="nav-pill">Collections</span>
                <span class="nav-pill">Environments</span>
                <span class="nav-pill">Docs</span>
            </div>
            <div class="nav-badge">
                <span class="badge-dot">All Systems Operational</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

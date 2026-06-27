import streamlit as st
from utils.sdk_templates import EXAMPLES


def render_examples_tab(api: dict):
    """Render the Examples tab with quick start, auth, and endpoint usage."""
    api_name = api.get("name", "GitHub REST API")
    examples = EXAMPLES.get(api_name, list(EXAMPLES.values())[0])

    st.markdown(
        """
        <div style="font-size:16px;font-weight:700;color:var(--text-primary);margin-bottom:6px">
            Integration Examples
        </div>
        <div style="font-size:13px;color:var(--text-muted);margin-bottom:24px">
            Ready-to-run code snippets to get you integrated quickly.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick Start
    with st.expander("🚀  Quick Start", expanded=True):
        st.markdown(
            """
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:12px;line-height:1.6">
                The minimal setup needed to make your first successful API call.
                Copy the snippet, replace the placeholder credentials, and run it.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.code(examples["quickstart"], language="python")
        col_qs_dl, _ = st.columns([2, 5])
        with col_qs_dl:
            st.download_button(
                "⬇  Download",
                data=examples["quickstart"],
                file_name=f"quickstart_{api_name.lower().replace(' ', '_')}.py",
                mime="text/plain",
                key="dl_qs",
            )

    # Authentication Example
    with st.expander("🔐  Authentication Example", expanded=False):
        st.markdown(
            """
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:12px;line-height:1.6">
                Demonstrates the correct way to pass credentials. Use environment variables
                for all secrets — never hard-code them in source files.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.code(examples["auth"], language="python")
        col_auth_dl, _ = st.columns([2, 5])
        with col_auth_dl:
            st.download_button(
                "⬇  Download",
                data=examples["auth"],
                file_name=f"auth_{api_name.lower().replace(' ', '_')}.py",
                mime="text/plain",
                key="dl_auth",
            )

    # Endpoint Usage
    with st.expander("🔗  Endpoint Usage Examples", expanded=False):
        st.markdown(
            """
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:12px;line-height:1.6">
                Practical examples covering the most commonly used endpoints,
                including pagination, request bodies, and error handling patterns.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.code(examples["endpoint_usage"], language="python")
        col_ep_dl, _ = st.columns([2, 5])
        with col_ep_dl:
            st.download_button(
                "⬇  Download",
                data=examples["endpoint_usage"],
                file_name=f"endpoints_{api_name.lower().replace(' ', '_')}.py",
                mime="text/plain",
                key="dl_ep",
            )

    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

    # Tips panel
    col_tip1, col_tip2, col_tip3 = st.columns(3)
    tips = [
        ("⏱️", "Rate Limiting",
         "Always handle 429 responses. Implement exponential back-off and respect Retry-After headers."),
        ("📝", "Error Handling",
         "Check HTTP status codes before parsing responses. Log raw error bodies for easier debugging."),
        ("🔄", "Pagination",
         "Most list endpoints are paginated. Always follow next-page links or use cursor-based iteration."),
    ]
    for col, (icon, title, body) in zip([col_tip1, col_tip2, col_tip3], tips):
        with col:
            st.markdown(
                f"""
                <div class="example-card">
                    <div style="font-size:24px;margin-bottom:10px">{icon}</div>
                    <div class="example-title">{title}</div>
                    <div class="example-desc">{body}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

import streamlit as st


_METHOD_BADGE = {
    "GET":    "badge-get",
    "POST":   "badge-post",
    "PUT":    "badge-put",
    "DELETE": "badge-delete",
    "PATCH":  "badge-patch",
}

_METHOD_ORDER = {"GET": 0, "POST": 1, "PUT": 2, "PATCH": 3, "DELETE": 4}


def render_endpoints_tab(api: dict):
    """Render the Endpoints tab with search, filter, and endpoint rows."""
    endpoints: list = api.get("endpoints", [])

    col_search, col_filter = st.columns([4, 1])
    with col_search:
        search = st.text_input(
            label="search_endpoints",
            label_visibility="collapsed",
            placeholder="🔍  Search endpoints by path or description…",
            key="endpoint_search",
        )
    with col_filter:
        methods_available = sorted(set(e["method"] for e in endpoints), key=lambda m: _METHOD_ORDER.get(m, 99))
        methods_available = ["All"] + methods_available
        method_filter = st.selectbox(
            label="method_filter",
            label_visibility="collapsed",
            options=methods_available,
            key="method_filter",
        )

    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

    # Filter logic
    filtered = endpoints
    if method_filter != "All":
        filtered = [e for e in filtered if e["method"] == method_filter]
    if search:
        q = search.lower()
        filtered = [e for e in filtered if q in e["path"].lower() or q in e.get("description", "").lower()]

    # Stats row
    st.markdown(
        f"""
        <div style="display:flex;gap:20px;margin-bottom:16px">
            <span style="font-size:13px;color:var(--text-muted)">
                Showing <strong style="color:var(--text-primary)">{len(filtered)}</strong>
                of <strong style="color:var(--text-primary)">{len(endpoints)}</strong> endpoints
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not filtered:
        st.markdown(
            """
            <div style="text-align:center;padding:40px 0;color:var(--text-muted);font-size:14px">
                No endpoints match your search criteria.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Column headers
    st.markdown(
        """
        <div style="display:grid;grid-template-columns:90px 1fr 1fr;gap:12px;
                    padding:8px 16px;border-bottom:1px solid var(--border);
                    font-size:11px;font-weight:600;color:var(--text-muted);
                    text-transform:uppercase;letter-spacing:0.8px;margin-bottom:4px">
            <span>Method</span>
            <span>Path</span>
            <span>Description</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Endpoint rows
    for ep in filtered:
        method    = ep.get("method", "GET")
        path      = ep.get("path", "/")
        desc      = ep.get("description", "")
        badge_cls = _METHOD_BADGE.get(method, "badge-get")

        st.markdown(
            f"""
            <div class="endpoint-row">
                <span class="{badge_cls}">{method}</span>
                <span class="endpoint-path">{path}</span>
                <span class="endpoint-desc">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    # Download as JSON
    import json
    col_dl, _ = st.columns([2, 3])
    with col_dl:
        st.download_button(
            label="⬇  Export Endpoints (JSON)",
            data=json.dumps(filtered, indent=2),
            file_name=f"{api.get('name', 'api').lower().replace(' ', '_')}_endpoints.json",
            mime="application/json",
            use_container_width=True,
        )

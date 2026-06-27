import streamlit as st


def render_overview_tab(api: dict):
    """Render the Overview tab content."""

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        # Description card
        st.markdown(
            f"""
            <div class="df-card">
                <div style="font-size:11px;font-weight:600;color:var(--text-muted);
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:12px">
                    About this API
                </div>
                <div style="font-size:14px;color:var(--text-secondary);line-height:1.7">
                    {api.get("description", "No description available.")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Key-value table
        st.markdown(
            """
            <div class="df-card">
                <div style="font-size:11px;font-weight:600;color:var(--text-muted);
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">
                    API Details
                </div>
            """,
            unsafe_allow_html=True,
        )

        rows = [
            ("API Name",              api.get("name", "—")),
            ("Base URL",              api.get("base_url", "—")),
            ("Version",               api.get("version", "—")),
            ("Authentication",        api.get("auth_type", "—")),
            ("Total Endpoints",       str(api.get("endpoints_count", len(api.get("endpoints", []))))),
            ("Documentation Source",  api.get("url", "—")),
            ("Status",                api.get("status", "Operational")),
            ("Last Updated",          api.get("last_updated", "—")),
        ]

        rows_html = ""
        for key, val in rows:
            val_cls = "url" if ("http" in val or "api." in val or "docs." in val) else ""
            rows_html += f"""
            <div class="kv-row">
                <div class="kv-key">{key}</div>
                <div class="kv-value {val_cls}">{val}</div>
            </div>
            """

        st.markdown(rows_html + "</div>", unsafe_allow_html=True)

    with col_right:
        # Status summary
        st.markdown(
            f"""
            <div class="df-card" style="text-align:center;padding:28px 20px">
                <div style="font-size:48px;margin-bottom:12px">✅</div>
                <div style="font-size:16px;font-weight:700;color:var(--text-primary);margin-bottom:6px">
                    Documentation Parsed
                </div>
                <div style="font-size:13px;color:var(--text-muted);margin-bottom:20px">
                    All endpoints and schemas extracted successfully
                </div>
                <div class="status-badge" style="display:inline-flex">
                    {api.get("status", "Operational")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Quick stats
        endpoints = api.get("endpoints", [])
        methods = [e["method"] for e in endpoints]
        method_counts = {m: methods.count(m) for m in set(methods)}

        st.markdown(
            """
            <div class="df-card">
                <div style="font-size:11px;font-weight:600;color:var(--text-muted);
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:14px">
                    Endpoint Methods
                </div>
            """,
            unsafe_allow_html=True,
        )

        method_colors = {
            "GET":    ("#10B981", "rgba(16,185,129,0.12)"),
            "POST":   ("#3B82F6", "rgba(59,130,246,0.12)"),
            "PUT":    ("#F59E0B", "rgba(245,158,11,0.12)"),
            "DELETE": ("#EF4444", "rgba(239,68,68,0.12)"),
            "PATCH":  ("#8B5CF6", "rgba(139,92,246,0.12)"),
        }

        bars_html = ""
        total = sum(method_counts.values()) or 1
        for method, count in sorted(method_counts.items(), key=lambda x: -x[1]):
            color, bg = method_colors.get(method, ("#9CA3AF", "rgba(156,163,175,0.12)"))
            pct = int((count / total) * 100)
            bars_html += f"""
            <div style="margin-bottom:12px">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                    <span style="font-size:12px;font-weight:700;color:{color}">{method}</span>
                    <span style="font-size:12px;color:var(--text-muted)">{count} endpoints</span>
                </div>
                <div style="height:6px;background:var(--border);border-radius:3px;overflow:hidden">
                    <div style="height:100%;width:{pct}%;background:{color};border-radius:3px;
                                transition:width 0.5s ease"></div>
                </div>
            </div>
            """

        st.markdown(bars_html + "</div>", unsafe_allow_html=True)

        # Auth type badge
        st.markdown(
            f"""
            <div class="df-card">
                <div style="font-size:11px;font-weight:600;color:var(--text-muted);
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:12px">
                    Authentication
                </div>
                <div class="auth-type-badge">🔐 {api.get("auth_type", "Unknown")}</div>
                <div style="font-size:12.5px;color:var(--text-muted);line-height:1.6;margin-top:8px">
                    {len(api.get("auth_headers", []))} required headers · 
                    Credentials must be included in every request.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

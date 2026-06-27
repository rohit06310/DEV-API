import streamlit as st


_AUTH_EXAMPLES = {
    "Bearer Token / OAuth 2.0": {
        "curl": """\
# cURL — Bearer Token
curl -H "Authorization: Bearer YOUR_TOKEN" \\
     -H "Accept: application/vnd.github+json" \\
     -H "X-GitHub-Api-Version: 2022-11-28" \\
     https://api.github.com/repos/octocat/Hello-World
""",
        "python": """\
import requests

headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

resp = requests.get("https://api.github.com/user", headers=headers)
print(resp.json())
""",
    },
    "HTTP Basic Auth (API Key)": {
        "curl": """\
# cURL — HTTP Basic Auth (Stripe)
curl -u sk_test_YOUR_KEY: \\
     -H "Stripe-Version: 2024-06-20" \\
     https://api.stripe.com/v1/balance
""",
        "python": """\
import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth("sk_test_YOUR_KEY", "")   # password is empty

resp = requests.get(
    "https://api.stripe.com/v1/balance",
    auth=auth,
    headers={"Stripe-Version": "2024-06-20"},
)
print(resp.json())
""",
    },
    "HTTP Basic Auth (Account SID + Auth Token)": {
        "curl": """\
# cURL — HTTP Basic Auth (Twilio)
ACCOUNT_SID="ACXXXXXXXXXXXXXXXX"
AUTH_TOKEN="your_auth_token"

curl -X GET "https://api.twilio.com/2010-04-01/Accounts/${ACCOUNT_SID}/Messages.json" \\
     -u "${ACCOUNT_SID}:${AUTH_TOKEN}"
""",
        "python": """\
import requests
from requests.auth import HTTPBasicAuth

ACCOUNT_SID = "ACXXXXXXXXXXXXXXXX"
AUTH_TOKEN  = "your_auth_token"

resp = requests.get(
    f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/Messages.json",
    auth=HTTPBasicAuth(ACCOUNT_SID, AUTH_TOKEN),
)
print(resp.json())
""",
    },
}


def render_authentication_tab(api: dict):
    """Render the Authentication tab."""
    auth_type    = api.get("auth_type", "Unknown")
    auth_headers = api.get("auth_headers", [])

    col_left, col_right = st.columns([5, 4], gap="large")

    with col_left:
        # Auth type
        st.markdown(
            f"""
            <div class="df-card">
                <div style="font-size:11px;font-weight:600;color:var(--text-muted);
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:14px">
                    Authentication Scheme
                </div>
                <div class="auth-type-badge">🔐 {auth_type}</div>
                <div style="margin-top:16px;font-size:13.5px;color:var(--text-secondary);line-height:1.7">
                    All requests to this API must include valid authentication credentials.
                    Missing or invalid credentials will return a <code style="color:#EF4444">401 Unauthorized</code> response.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Required headers
        st.markdown(
            """
            <div class="df-card">
                <div style="font-size:11px;font-weight:600;color:var(--text-muted);
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:14px">
                    Required Headers
                </div>
            """,
            unsafe_allow_html=True,
        )

        col_h_name, col_h_val, col_h_req = st.columns([2, 3, 1])
        with col_h_name:
            st.markdown('<div style="font-size:11px;color:var(--text-muted);font-weight:600;text-transform:uppercase;letter-spacing:0.6px">Header</div>', unsafe_allow_html=True)
        with col_h_val:
            st.markdown('<div style="font-size:11px;color:var(--text-muted);font-weight:600;text-transform:uppercase;letter-spacing:0.6px">Value / Format</div>', unsafe_allow_html=True)
        with col_h_req:
            st.markdown('<div style="font-size:11px;color:var(--text-muted);font-weight:600;text-transform:uppercase;letter-spacing:0.6px">Required</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:1px;background:var(--border);margin:8px 0 12px"></div>', unsafe_allow_html=True)

        for hdr in auth_headers:
            req_badge = (
                '<span style="color:#10B981;font-weight:600;font-size:11px">● Yes</span>'
                if hdr.get("required")
                else '<span style="color:var(--text-muted);font-size:11px">○ No</span>'
            )
            col_h_name, col_h_val, col_h_req = st.columns([2, 3, 1])
            with col_h_name:
                st.markdown(f'<div style="font-family:var(--font-mono);font-size:12.5px;color:#93C5FD;padding:4px 0">{hdr["key"]}</div>', unsafe_allow_html=True)
            with col_h_val:
                st.markdown(f'<div style="font-family:var(--font-mono);font-size:12px;color:var(--text-muted);padding:4px 0">{hdr["value"]}</div>', unsafe_allow_html=True)
            with col_h_req:
                st.markdown(f'<div style="padding:4px 0">{req_badge}</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # Authorization examples
        examples = _AUTH_EXAMPLES.get(auth_type, list(_AUTH_EXAMPLES.values())[0])

        st.markdown(
            """
            <div style="font-size:11px;font-weight:600;color:var(--text-muted);
                        text-transform:uppercase;letter-spacing:1px;margin-bottom:14px">
                Authorization Examples
            </div>
            """,
            unsafe_allow_html=True,
        )

        ex_tab_curl, ex_tab_py = st.tabs(["  cURL  ", "  Python  "])
        with ex_tab_curl:
            st.code(examples["curl"], language="bash")
        with ex_tab_py:
            st.code(examples["python"], language="python")

        # Security tips
        st.markdown(
            """
            <div class="df-card" style="margin-top:16px">
                <div style="font-size:11px;font-weight:600;color:var(--text-muted);
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:12px">
                    Security Best Practices
                </div>
                <div style="font-size:13px;color:var(--text-secondary);line-height:1.8">
                    🔒&nbsp; Store credentials in environment variables, never in source code.<br>
                    🔄&nbsp; Rotate API keys regularly and revoke unused credentials.<br>
                    🛡️&nbsp; Use scoped/restricted keys with minimal permissions.<br>
                    📋&nbsp; Monitor API key usage for anomalies in your dashboard.<br>
                    🚫&nbsp; Never commit <code style="color:#EF4444">.env</code> files or secrets to version control.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

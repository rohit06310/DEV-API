import streamlit as st


# ── Preset API catalog ────────────────────────────────────────────────────────

PRESET_APIS = {
    "GitHub REST API": {
        "url": "https://docs.github.com/en/rest",
        "name": "GitHub REST API",
        "version": "v3 / 2022-11-28",
        "base_url": "https://api.github.com",
        "auth_type": "Bearer Token / OAuth 2.0",
        "description": "The GitHub REST API provides programmatic access to GitHub data. Interact with repositories, commits, issues, pull requests, and more.",
        "endpoints_count": 247,
        "status": "Operational",
        "last_updated": "2024-12-01",
        "endpoints": [
            {"method": "GET",    "path": "/repos/{owner}/{repo}",              "description": "Get a repository"},
            {"method": "GET",    "path": "/repos/{owner}/{repo}/commits",       "description": "List commits"},
            {"method": "POST",   "path": "/repos/{owner}/{repo}/issues",        "description": "Create an issue"},
            {"method": "GET",    "path": "/repos/{owner}/{repo}/pulls",         "description": "List pull requests"},
            {"method": "PATCH",  "path": "/repos/{owner}/{repo}/issues/{n}",   "description": "Update an issue"},
            {"method": "DELETE", "path": "/repos/{owner}/{repo}/git/refs/{r}",  "description": "Delete a reference"},
            {"method": "GET",    "path": "/users/{username}",                   "description": "Get a user"},
            {"method": "GET",    "path": "/orgs/{org}/members",                 "description": "List org members"},
            {"method": "POST",   "path": "/repos/{owner}/{repo}/forks",         "description": "Create a fork"},
            {"method": "GET",    "path": "/search/repositories",               "description": "Search repositories"},
            {"method": "GET",    "path": "/rate_limit",                         "description": "Get rate limit status"},
            {"method": "PUT",    "path": "/repos/{owner}/{repo}/collaborators/{u}", "description": "Add collaborator"},
        ],
        "auth_headers": [
            {"key": "Authorization", "value": "Bearer <your_token>",             "required": True},
            {"key": "Accept",        "value": "application/vnd.github+json",    "required": True},
            {"key": "X-GitHub-Api-Version", "value": "2022-11-28",              "required": False},
        ],
    },
    "Stripe API": {
        "url": "https://stripe.com/docs/api",
        "name": "Stripe API",
        "version": "2024-06-20",
        "base_url": "https://api.stripe.com/v1",
        "auth_type": "HTTP Basic Auth (API Key)",
        "description": "Stripe's API is organized around REST. It uses HTTP response codes to indicate errors and returns JSON for all responses.",
        "endpoints_count": 312,
        "status": "Operational",
        "last_updated": "2024-11-15",
        "endpoints": [
            {"method": "POST",   "path": "/charges",                  "description": "Create a charge"},
            {"method": "GET",    "path": "/charges/{id}",             "description": "Retrieve a charge"},
            {"method": "GET",    "path": "/charges",                  "description": "List all charges"},
            {"method": "POST",   "path": "/customers",                "description": "Create a customer"},
            {"method": "GET",    "path": "/customers/{id}",           "description": "Retrieve a customer"},
            {"method": "POST",   "path": "/payment_intents",          "description": "Create a payment intent"},
            {"method": "POST",   "path": "/refunds",                  "description": "Create a refund"},
            {"method": "GET",    "path": "/balance",                  "description": "Retrieve balance"},
            {"method": "POST",   "path": "/subscriptions",            "description": "Create a subscription"},
            {"method": "DELETE", "path": "/subscriptions/{id}",       "description": "Cancel a subscription"},
            {"method": "GET",    "path": "/products",                 "description": "List all products"},
            {"method": "POST",   "path": "/prices",                   "description": "Create a price"},
        ],
        "auth_headers": [
            {"key": "Authorization", "value": "Basic sk_live_<api_key>:",       "required": True},
            {"key": "Content-Type",  "value": "application/x-www-form-urlencoded", "required": True},
            {"key": "Stripe-Version", "value": "2024-06-20",                   "required": False},
        ],
    },
    "Twilio API": {
        "url": "https://www.twilio.com/docs/usage/api",
        "name": "Twilio API",
        "version": "2010-04-01",
        "base_url": "https://api.twilio.com/2010-04-01",
        "auth_type": "HTTP Basic Auth (Account SID + Auth Token)",
        "description": "The Twilio REST API allows you to make and receive calls, send and receive messages, and perform other communication functions.",
        "endpoints_count": 89,
        "status": "Operational",
        "last_updated": "2024-10-20",
        "endpoints": [
            {"method": "POST",  "path": "/Accounts/{Sid}/Messages",              "description": "Send an SMS"},
            {"method": "GET",   "path": "/Accounts/{Sid}/Messages/{Sid}",        "description": "Get message details"},
            {"method": "GET",   "path": "/Accounts/{Sid}/Messages",              "description": "List messages"},
            {"method": "POST",  "path": "/Accounts/{Sid}/Calls",                 "description": "Make a call"},
            {"method": "GET",   "path": "/Accounts/{Sid}/Calls/{Sid}",           "description": "Get call details"},
            {"method": "POST",  "path": "/Accounts/{Sid}/IncomingPhoneNumbers",  "description": "Buy a phone number"},
            {"method": "GET",   "path": "/Accounts/{Sid}/IncomingPhoneNumbers",  "description": "List phone numbers"},
            {"method": "DELETE","path": "/Accounts/{Sid}/IncomingPhoneNumbers/{Sid}", "description": "Release number"},
            {"method": "POST",  "path": "/Accounts/{Sid}/Recordings",           "description": "Start recording"},
            {"method": "GET",   "path": "/Accounts/{Sid}/Usage/Records",        "description": "Usage records"},
        ],
        "auth_headers": [
            {"key": "Authorization", "value": "Basic base64(<AccountSid>:<AuthToken>)", "required": True},
            {"key": "Content-Type",  "value": "application/x-www-form-urlencoded",     "required": True},
        ],
    },
}


def init_session_state():
    """Initialise all session state keys with defaults."""
    defaults = {
        "analyzed":         False,
        "analyzing":        False,
        "api_url":          "",
        "api_data":         None,
        "active_tab":       "Overview",
        "search_query":     "",
        "selected_lang":    "Python",
        "analysis_progress": 0,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

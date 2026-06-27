import streamlit as st


def apply_custom_css():
    """Inject all custom CSS for the DevFlow dark theme."""
    st.markdown(
        """
        <style>
        /* ── Google Fonts ─────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* ── CSS Variables ────────────────────────────────────────── */
        :root {
            --bg-primary:    #0B1220;
            --bg-card:       #111827;
            --bg-card-hover: #151f30;
            --bg-input:      #0d1829;
            --border:        #1F2937;
            --border-focus:  #3B82F6;
            --accent:        #3B82F6;
            --accent-hover:  #2563EB;
            --accent-glow:   rgba(59,130,246,0.25);
            --text-primary:  #F9FAFB;
            --text-secondary:#9CA3AF;
            --text-muted:    #6B7280;
            --success:       #10B981;
            --warning:       #F59E0B;
            --danger:        #EF4444;
            --font-sans:     'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono:     'JetBrains Mono', 'Fira Code', monospace;
            --radius-sm:     6px;
            --radius-md:     10px;
            --radius-lg:     14px;
            --shadow-card:   0 1px 3px rgba(0,0,0,0.4), 0 4px 20px rgba(0,0,0,0.25);
        }

        /* ── Global Reset ─────────────────────────────────────────── */
        html, body, [class*="css"] {
            font-family: var(--font-sans) !important;
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }

        /* Hide Streamlit chrome */
        #MainMenu, footer, header { visibility: hidden; }
        .stDeployButton { display: none; }
        [data-testid="stToolbar"] { display: none; }
        [data-testid="stDecoration"] { display: none; }

        /* Remove default padding */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }

        /* ── Scrollbar ────────────────────────────────────────────── */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #374151; }

        /* ── Top Navbar ───────────────────────────────────────────── */
        .devflow-navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 32px;
            height: 58px;
            background: rgba(11,18,32,0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 999;
        }
        .devflow-logo {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .devflow-logo-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #3B82F6, #8B5CF6);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            box-shadow: 0 0 20px rgba(59,130,246,0.4);
        }
        .devflow-logo-text {
            font-size: 18px;
            font-weight: 700;
            letter-spacing: -0.3px;
            color: var(--text-primary);
        }
        .devflow-logo-text span { color: var(--accent); }
        .devflow-tagline {
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 400;
            letter-spacing: 0.5px;
        }
        .nav-pills {
            display: flex;
            gap: 4px;
        }
        .nav-pill {
            padding: 6px 14px;
            border-radius: var(--radius-sm);
            font-size: 13px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s ease;
            border: none;
            background: transparent;
        }
        .nav-pill:hover { background: var(--border); color: var(--text-primary); }
        .nav-pill.active { background: rgba(59,130,246,0.15); color: var(--accent); }
        .nav-badge {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .badge-dot {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: var(--success);
            font-weight: 500;
        }
        .badge-dot::before {
            content: '';
            width: 7px;
            height: 7px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--success);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* ── Main Layout ──────────────────────────────────────────── */
        .devflow-main {
            display: grid;
            grid-template-columns: 280px 1fr;
            height: calc(100vh - 58px);
        }

        /* ── Sidebar ──────────────────────────────────────────────── */
        .devflow-sidebar {
            background: var(--bg-card);
            border-right: 1px solid var(--border);
            padding: 24px 0;
            overflow-y: auto;
        }
        .sidebar-section {
            padding: 0 16px;
            margin-bottom: 28px;
        }
        .sidebar-label {
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 1px;
            color: var(--text-muted);
            text-transform: uppercase;
            margin-bottom: 10px;
            padding: 0 8px;
        }
        .sidebar-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 9px 12px;
            border-radius: var(--radius-sm);
            font-size: 13.5px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s ease;
            margin-bottom: 2px;
            border: 1px solid transparent;
        }
        .sidebar-item:hover { background: rgba(59,130,246,0.08); color: var(--text-primary); }
        .sidebar-item.active {
            background: rgba(59,130,246,0.12);
            color: var(--accent);
            border-color: rgba(59,130,246,0.2);
        }
        .sidebar-icon { font-size: 15px; width: 18px; text-align: center; }

        /* ── Cards ────────────────────────────────────────────────── */
        .df-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 20px;
            box-shadow: var(--shadow-card);
            margin-bottom: 16px;
            transition: border-color 0.2s ease;
        }
        .df-card:hover { border-color: #374151; }

        /* ── Stat Cards ───────────────────────────────────────────── */
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 16px;
            text-align: left;
            transition: all 0.2s ease;
            cursor: default;
        }
        .stat-card:hover {
            border-color: var(--accent);
            box-shadow: 0 0 0 1px var(--accent-glow);
        }
        .stat-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; margin-bottom: 8px; }
        .stat-value { font-size: 26px; font-weight: 700; color: var(--text-primary); line-height: 1; }
        .stat-sub   { font-size: 12px; color: var(--text-secondary); margin-top: 4px; }
        .stat-accent { color: var(--accent); }

        /* ── Input & Buttons ──────────────────────────────────────── */
        .stTextInput > div > div > input {
            background: var(--bg-input) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-mono) !important;
            font-size: 13.5px !important;
            padding: 12px 16px !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: var(--border-focus) !important;
            box-shadow: 0 0 0 3px var(--accent-glow) !important;
        }
        .stTextInput > div > div > input::placeholder { color: var(--text-muted) !important; }

        /* Primary Button */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 12px 28px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 15px rgba(59,130,246,0.35) !important;
            letter-spacing: 0.2px !important;
        }
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(59,130,246,0.5) !important;
            background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        }
        .stButton > button[kind="primary"]:active { transform: translateY(0) !important; }

        /* Secondary button */
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-size: 13px !important;
            padding: 8px 18px !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button[kind="secondary"]:hover {
            border-color: var(--accent) !important;
            color: var(--accent) !important;
            background: rgba(59,130,246,0.05) !important;
        }

        /* ── Tabs ─────────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            background: transparent !important;
            border-bottom: 1px solid var(--border) !important;
            gap: 0 !important;
            padding: 0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border: none !important;
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-size: 13.5px !important;
            padding: 12px 20px !important;
            border-bottom: 2px solid transparent !important;
            transition: all 0.15s ease !important;
            margin-bottom: -1px !important;
        }
        .stTabs [data-baseweb="tab"]:hover { color: var(--text-primary) !important; }
        .stTabs [aria-selected="true"] {
            color: var(--accent) !important;
            border-bottom-color: var(--accent) !important;
            background: transparent !important;
        }
        .stTabs [data-baseweb="tab-panel"] {
            padding: 24px 0 !important;
            background: transparent !important;
        }

        /* ── Selectbox ────────────────────────────────────────────── */
        .stSelectbox > div > div {
            background: var(--bg-input) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-primary) !important;
        }
        .stSelectbox > div > div:focus-within { border-color: var(--border-focus) !important; }

        /* ── Code blocks ──────────────────────────────────────────── */
        .stCodeBlock {
            background: #060d1a !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
        }
        code {
            font-family: var(--font-mono) !important;
            font-size: 13px !important;
        }

        /* ── Progress / Spinner ───────────────────────────────────── */
        .stSpinner > div { border-top-color: var(--accent) !important; }
        .stProgress > div > div > div {
            background: linear-gradient(90deg, var(--accent), #8B5CF6) !important;
        }

        /* ── Table / DataFrame ────────────────────────────────────── */
        .stDataFrame {
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            overflow: hidden !important;
        }
        [data-testid="stDataFrameResizable"] thead tr th {
            background: #0d1829 !important;
            color: var(--text-muted) !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.8px !important;
            border-bottom: 1px solid var(--border) !important;
        }
        [data-testid="stDataFrameResizable"] tbody tr td {
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
            border-bottom: 1px solid var(--border) !important;
            font-family: var(--font-mono) !important;
            font-size: 13px !important;
        }
        [data-testid="stDataFrameResizable"] tbody tr:hover td { background: var(--bg-card-hover) !important; }

        /* ── Method Badges ────────────────────────────────────────── */
        .badge-get    { background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.3); padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; font-family: var(--font-mono); }
        .badge-post   { background: rgba(59,130,246,0.15); color: #3B82F6; border: 1px solid rgba(59,130,246,0.3); padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; font-family: var(--font-mono); }
        .badge-put    { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.3); padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; font-family: var(--font-mono); }
        .badge-delete { background: rgba(239,68,68,0.15);  color: #EF4444; border: 1px solid rgba(239,68,68,0.3);  padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; font-family: var(--font-mono); }
        .badge-patch  { background: rgba(139,92,246,0.15); color: #8B5CF6; border: 1px solid rgba(139,92,246,0.3); padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; font-family: var(--font-mono); }

        /* ── Info / Alert boxes ───────────────────────────────────── */
        .stAlert { border-radius: var(--radius-md) !important; border: none !important; }
        .stInfo   { background: rgba(59,130,246,0.1) !important; color: #93C5FD !important; }
        .stSuccess { background: rgba(16,185,129,0.1) !important; color: #6EE7B7 !important; }
        .stWarning { background: rgba(245,158,11,0.1) !important; color: #FCD34D !important; }

        /* ── Section headers ──────────────────────────────────────── */
        .section-header {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .section-header::after {
            content: '';
            flex: 1;
            height: 1px;
            background: var(--border);
        }

        /* ── Recent API chips ─────────────────────────────────────── */
        .recent-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 5px 14px;
            font-size: 12.5px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s ease;
            margin: 4px 4px 4px 0;
            font-weight: 500;
        }
        .recent-chip:hover { border-color: var(--accent); color: var(--accent); background: rgba(59,130,246,0.06); }

        /* ── Loading overlay ──────────────────────────────────────── */
        .loading-step {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 20px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            margin-bottom: 10px;
            font-size: 14px;
            color: var(--text-secondary);
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .loading-step.active { border-color: var(--accent); color: var(--text-primary); background: rgba(59,130,246,0.06); }
        .loading-step.done   { border-color: var(--success); color: var(--success); }
        .loading-dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; }

        /* ── Auth badge ───────────────────────────────────────────── */
        .auth-type-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(139,92,246,0.12);
            border: 1px solid rgba(139,92,246,0.3);
            color: #A78BFA;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 16px;
        }

        /* ── Status Badge ─────────────────────────────────────────── */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16,185,129,0.12);
            border: 1px solid rgba(16,185,129,0.3);
            color: #34D399;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-badge::before {
            content: '';
            width: 6px;
            height: 6px;
            background: currentColor;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        /* ── Key-value rows ───────────────────────────────────────── */
        .kv-row {
            display: flex;
            align-items: flex-start;
            gap: 0;
            padding: 12px 0;
            border-bottom: 1px solid var(--border);
            font-size: 13.5px;
        }
        .kv-row:last-child { border-bottom: none; }
        .kv-key   { color: var(--text-muted); font-weight: 500; width: 180px; flex-shrink: 0; }
        .kv-value { color: var(--text-primary); font-family: var(--font-mono); font-size: 13px; }
        .kv-value.url { color: var(--accent); }

        /* ── Separator ────────────────────────────────────────────── */
        .df-divider { height: 1px; background: var(--border); margin: 20px 0; }

        /* ── Stale sidebar ────────────────────────────────────────── */
        [data-testid="stSidebar"] { display: none; }

        /* ── Content wrapper ──────────────────────────────────────── */
        .content-area {
            padding: 28px 32px;
            overflow-y: auto;
            height: calc(100vh - 58px);
            background: var(--bg-primary);
        }

        /* ── Empty state ──────────────────────────────────────────── */
        .empty-state {
            text-align: center;
            padding: 64px 32px;
        }
        .empty-icon {
            font-size: 56px;
            margin-bottom: 20px;
            opacity: 0.6;
        }
        .empty-title {
            font-size: 22px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 10px;
        }
        .empty-subtitle {
            font-size: 14px;
            color: var(--text-muted);
            max-width: 420px;
            margin: 0 auto 28px;
            line-height: 1.6;
        }

        /* ── Endpoint row ─────────────────────────────────────────── */
        .endpoint-row {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 12px 16px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            margin-bottom: 8px;
            transition: all 0.15s ease;
            cursor: pointer;
        }
        .endpoint-row:hover { border-color: #374151; background: var(--bg-card-hover); }
        .endpoint-path {
            font-family: var(--font-mono);
            font-size: 13px;
            color: var(--text-primary);
            flex: 1;
        }
        .endpoint-desc {
            font-size: 12.5px;
            color: var(--text-muted);
            text-align: right;
        }

        /* ── Header field ─────────────────────────────────────────── */
        .header-field {
            background: #060d1a;
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 10px 16px;
            font-family: var(--font-mono);
            font-size: 13px;
            color: #93C5FD;
            margin-bottom: 8px;
        }
        .header-key   { color: var(--text-muted); }
        .header-value { color: #93C5FD; }

        /* ── SDK tabs ─────────────────────────────────────────────── */
        .lang-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .lang-btn.active, .lang-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
            background: rgba(59,130,246,0.08);
        }

        /* ── Example card ─────────────────────────────────────────── */
        .example-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 20px;
            margin-bottom: 16px;
        }
        .example-title {
            font-size: 15px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 4px;
        }
        .example-desc {
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 14px;
        }

        /* ── Metric override ──────────────────────────────────────── */
        [data-testid="stMetricValue"] { color: var(--text-primary) !important; font-size: 28px !important; font-weight: 700 !important; }
        [data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 12px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.6px; }
        [data-testid="stMetricDelta"] { font-size: 12px !important; }
        div[data-testid="metric-container"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            padding: 16px 20px !important;
        }

        /* ── Divider ──────────────────────────────────────────────── */
        hr { border-color: var(--border) !important; }

        /* ── Column gaps ──────────────────────────────────────────── */
        [data-testid="column"] { padding: 0 8px !important; }

        </style>
        """,
        unsafe_allow_html=True,
    )

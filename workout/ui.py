from workout.plots import ACCENT, BG, PANEL, TEXT, SUBTEXT, GRID

CSS = f"""
<style>
    .stApp {{ background-color: {BG}; }}
    [data-testid="stSidebarCollapsedControl"] {{ display: none; }}
    .metric-card {{
        background: {PANEL};
        border: 1px solid {GRID};
        border-radius: 10px;
        padding: 18px 22px;
        text-align: center;
    }}
    .metric-value {{ font-size: 2rem; font-weight: 700; color: {ACCENT}; margin: 0; }}
    .metric-label {{ font-size: 0.78rem; color: {SUBTEXT}; text-transform: uppercase; letter-spacing: 0.08em; margin: 0; }}
    .metric-sub {{ font-size: 0.85rem; color: {TEXT}; margin: 4px 0 0 0; }}
    h1, h2, h3, p, label, .stMarkdown {{ color: {TEXT} !important; }}
    .stTabs [data-baseweb="tab"] {{ color: {SUBTEXT}; }}
    .stTabs [aria-selected="true"] {{ color: {TEXT}; border-bottom-color: {ACCENT}; }}
    div[data-testid="stSelectbox"] label, div[data-testid="stDateInput"] label,
    div[data-testid="stMultiSelect"] label {{ color: {TEXT} !important; }}
</style>
"""


def kpi(value, label, sub=""):
    return f"""
    <div class="metric-card">
        <p class="metric-value">{value}</p>
        <p class="metric-label">{label}</p>
        {"<p class='metric-sub'>" + sub + "</p>" if sub else ""}
    </div>"""

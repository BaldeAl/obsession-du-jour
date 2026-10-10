from __future__ import annotations

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

:root {
    --bg-main: #0c0e12;
    --bg-card: #151820;
    --bg-card-subtle: #1c202a;
    --border-card: rgba(255, 255, 255, 0.08);
    --border-highlight: rgba(255, 255, 255, 0.16);
    --text-primary: #f3f5f8;
    --text-muted: #8b93a3;
    --accent-mono: #ffffff;
    --shadow-3d: 0 4px 0 #090b0e, 0 10px 24px rgba(0, 0, 0, 0.45);
    --inset-glow: inset 0 1px 1px rgba(255, 255, 255, 0.12);
}

.stApp {
    background-color: var(--bg-main);
    color: var(--text-primary);
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text-primary);
    letter-spacing: -0.03em;
}

.hero-box {
    background: linear-gradient(180deg, #191c25 0%, #12141a 100%);
    border: 1px solid var(--border-card);
    border-radius: 24px;
    padding: 26px 32px;
    margin-bottom: 24px;
    box-shadow: 0 8px 0 #08090c, 0 16px 32px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.15);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 999px;
    background: #232733;
    border: 1px solid var(--border-highlight);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #e2e6f0;
    text-transform: uppercase;
    box-shadow: 0 2px 0 #0d0f14;
}

.status-card {
    background: linear-gradient(180deg, #1b1f29 0%, #13161e 100%);
    border: 1px solid var(--border-card);
    border-radius: 20px;
    padding: 20px 24px;
    box-shadow: var(--shadow-3d), var(--inset-glow);
    margin-bottom: 20px;
}

.status-badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    background: #272d3b;
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 3px 0 #0e1117;
}

.gauge-container {
    width: 100%;
    background: #0f1116;
    border-radius: 999px;
    height: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.6);
    overflow: hidden;
    margin: 12px 0 8px 0;
}

.gauge-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #5a6475 0%, #ffffff 100%);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
    transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

[data-testid="stMetric"] {
    background: linear-gradient(180deg, #171b23 0%, #12141a 100%) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: 20px !important;
    padding: 16px 20px !important;
    box-shadow: 0 5px 0 #090b0e, 0 10px 20px rgba(0, 0, 0, 0.35), var(--inset-glow) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 0 #090b0e, 0 14px 26px rgba(0, 0, 0, 0.45), var(--inset-glow) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.85rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.03em !important;
}

.stButton > button {
    background: linear-gradient(180deg, #242936 0%, #1a1e28 100%) !important;
    color: #f1f3f7 !important;
    font-weight: 600 !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 14px !important;
    padding: 8px 18px !important;
    box-shadow: 0 4px 0 #0d0f14, 0 8px 16px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    transition: all 0.1s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(180deg, #2c3242 0%, #1f2430 100%) !important;
    color: #ffffff !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
    transform: translateY(-1px);
    box-shadow: 0 5px 0 #0d0f14, 0 10px 20px rgba(0, 0, 0, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(3px) !important;
    box-shadow: 0 1px 0 #0d0f14, 0 2px 4px rgba(0, 0, 0, 0.2) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: transparent;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 14px !important;
    padding: 10px 20px !important;
    background: #14171e !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    box-shadow: 0 3px 0 #0a0c0f !important;
    transition: all 0.15s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    border-color: rgba(255, 255, 255, 0.15) !important;
}

.stTabs [aria-selected="true"] {
    background: #252a37 !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 4px 0 #0d0f14, inset 0 1px 0 rgba(255,255,255,0.2) !important;
}

[data-testid="stSidebar"] {
    background-color: #0f1117 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
}

.content-card {
    background: linear-gradient(180deg, #151820 0%, #111319 100%);
    border: 1px solid var(--border-card);
    border-radius: 22px;
    padding: 22px;
    box-shadow: var(--shadow-3d), var(--inset-glow);
    margin-bottom: 24px;
}

.quick-picks-label {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 8px;
}
</style>
"""

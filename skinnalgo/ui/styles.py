"""
Apple/iOS Luxury Styling System for SkinnAlgo.
Implements dark obsidian aesthetics, subtle ambient gradients, and crisp typography.
"""

LUXURY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap');

html, body, [class*="css"], [class*="st-"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #F1F5F9;
}

/* Base App Obsidian Background */
.stApp {
    background-color: #0c0d12 !important;
    background-image: 
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99, 102, 241, 0.12) 0%, rgba(12, 13, 18, 0.98) 60%, #090a0e 100%) !important;
    background-attachment: fixed !important;
}

/* Precision Sleek Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: #1e2230;
    border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
    background: #31384e;
}

/* Flagship Header & Branding */
.brand-hero-container {
    text-align: center;
    margin-top: 1.5rem;
    margin-bottom: 2rem;
    animation: heroFadeIn 0.4s ease-out;
}
@keyframes heroFadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

.brand-avatar-wrapper {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 68px;
    height: 68px;
    border-radius: 20px;
    background: radial-gradient(circle at 50% 30%, rgba(99, 102, 241, 0.25) 0%, rgba(20, 22, 32, 0.95) 75%);
    border: 1px solid rgba(99, 102, 241, 0.4);
    box-shadow: 0 0 32px rgba(99, 102, 241, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.15);
    margin-bottom: 16px;
}

.brand-title {
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -0.035em;
    color: #F8FAFC;
    margin-bottom: 0.3rem;
}

.brand-subtitle {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Plus Jakarta Sans", sans-serif;
    font-size: 1.05rem;
    color: #94A3B8;
    margin-bottom: 1.2rem;
    letter-spacing: -0.01em;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
}

/* Flagship Feature Action Cards */
.hero-action-card {
    background: rgba(20, 23, 33, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.85rem;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.hero-action-card:hover {
    background: rgba(26, 30, 44, 0.85);
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateY(-1px);
    box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.5);
}

/* Glassmorphism Card Container */
.luxury-card {
    background: #131620;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
    transition: border-color 0.2s ease;
}

.luxury-card:hover {
    border-color: #383F54;
}

/* KPI Metric Meter Box */
.metric-box {
    background: #10131A;
    border: 1px solid #1E2330;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: left;
}

.metric-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
    font-weight: 600;
    margin-bottom: 0.3rem;
}

.metric-val {
    font-size: 1.65rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #F8FAFC;
    line-height: 1.2;
}

.metric-subtitle {
    font-size: 0.78rem;
    color: #94A3B8;
    margin-top: 0.25rem;
}

/* Status Pills */
.pill-badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

.pill-cyan {
    background: rgba(6, 182, 212, 0.12);
    color: #22D3EE;
    border: 1px solid rgba(6, 182, 212, 0.3);
}

.pill-violet {
    background: rgba(139, 92, 246, 0.12);
    color: #A78BFA;
    border: 1px solid rgba(139, 92, 246, 0.3);
}

.pill-emerald {
    background: rgba(16, 185, 129, 0.12);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.pill-rose {
    background: rgba(244, 63, 94, 0.12);
    color: #FB7185;
    border: 1px solid rgba(244, 63, 94, 0.3);
}

.pill-amber {
    background: rgba(245, 158, 11, 0.12);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

/* Routine Step Timeline Card */
.routine-step {
    background: #141720;
    border-left: 3px solid #6366F1;
    border-top: 1px solid #232734;
    border-right: 1px solid #232734;
    border-bottom: 1px solid #232734;
    border-radius: 0 12px 12px 0;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
}

.step-num {
    font-size: 0.75rem;
    font-weight: 700;
    color: #818CF8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.step-compound {
    font-size: 1.15rem;
    font-weight: 600;
    color: #F8FAFC;
    margin: 0.15rem 0 0.3rem 0;
}

.step-moa {
    font-size: 0.84rem;
    color: #94A3B8;
    line-height: 1.5;
    margin-bottom: 0.6rem;
}

.search-box {
    background: #0B0D13;
    border: 1px solid #1E2330;
    border-radius: 6px;
    padding: 0.45rem 0.75rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.76rem;
    color: #38BDF8;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Sleek Luxury Button Styling */
.stButton > button {
    background: linear-gradient(180deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stButton > button:hover {
    background: linear-gradient(180deg, #6366F1 0%, #4F46E5 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Tabs Header */
.stTabs [data-baseweb="tab-list"] {
    gap: 1.5rem;
    border-bottom: 1px solid #1E2330;
    padding-bottom: 0.3rem;
}

.stTabs [data-baseweb="tab"] {
    color: #64748B;
    font-weight: 500;
    font-size: 0.92rem;
    padding: 0.5rem 0;
    background-color: transparent !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    color: #F8FAFC !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #6366F1 !important;
}

/* Remove default Streamlit top padding & preserve sidebar toggle header */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}

header {
    background-color: transparent !important;
}
[data-testid="stDecoration"] {
    display: none !important;
}
[data-testid="stToolbar"] {
    visibility: hidden !important;
}
footer {
    display: none !important;
}
</style>
"""


def inject_luxury_styles():
    """Inject luxury CSS into the Streamlit session."""
    import streamlit as st
    st.markdown(LUXURY_CSS, unsafe_allow_html=True)


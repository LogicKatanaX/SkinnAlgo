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
    background-color: #0A0B0E;
    background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.05) 0px, transparent 50%);
}

/* Header & Serif Title */
.brand-title {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #FFFFFF 30%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.brand-subtitle {
    font-family: 'Newsreader', Georgia, serif;
    font-style: italic;
    font-size: 1.15rem;
    color: #94A3B8;
    margin-bottom: 1.8rem;
    letter-spacing: 0.01em;
}

/* Glassmorphism Card Container */
.luxury-card {
    background: #14171F;
    border: 1px solid #232734;
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

/* Primary Button Styling */
.stButton > button {
    background: #4F46E5 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.55rem 1.4rem !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: #4338CA !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.45) !important;
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

/* Remove default Streamlit top padding */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}

header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""


def inject_luxury_styles():
    """Inject luxury CSS into the Streamlit session."""
    import streamlit as st
    st.markdown(LUXURY_CSS, unsafe_allow_html=True)


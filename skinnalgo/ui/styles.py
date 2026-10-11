"""
Coastal Marine & Sea-Blue / Sea-Green Biotech Styling System for SkinnAlgo.
Implements light aquatic luxury aesthetic, crystal clear ocean typography, and zero dark mode.
"""

LUXURY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap');

html {
    scroll-behavior: smooth;
}

html, body, p, h1, h2, h3, h4, h5, h6, label, input, textarea, select, button, div.stMarkdown, div.stText {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0F172A;
}

/* Ensure Streamlit Material Icon ligatures and SVGs are never overridden */
[data-testid*="Icon"], [class*="material-symbols"], span[class*="stIcon"], .material-symbols-rounded {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
}

/* Fix File Uploader Button layout & icon alignment */
[data-testid="stFileUploaderDropzone"] button {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    white-space: nowrap !important;
    background: linear-gradient(135deg, #0284C7 0%, #0D9488 100%) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    border: none !important;
}

/* File Uploader Dropzone Container (Zero Dark Mode) */
[data-testid="stFileUploaderDropzone"] {
    background-color: #FFFFFF !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%) !important;
    border: 2px dashed rgba(14, 165, 233, 0.35) !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
    box-shadow: 0 4px 16px rgba(14, 165, 233, 0.05) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #0284C7 !important;
    background: #F0F9FF !important;
}

[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] div {
    color: #334155 !important;
}

[data-testid="stFileUploaderDropzone"] small {
    color: #64748B !important;
    font-size: 0.8rem !important;
}

[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] * {
    color: #475569 !important;
}

[data-testid="stFileUploaderFileData"] {
    background-color: #F0F9FF !important;
    border: 1px solid rgba(14, 165, 233, 0.25) !important;
    border-radius: 10px !important;
    color: #0F172A !important;
}

[data-testid="stFileUploaderFileData"] * {
    color: #0F172A !important;
}

[data-testid="stFileUploaderDeleteBtn"] button {
    background: transparent !important;
    border: none !important;
    color: #64748B !important;
}

[data-testid="stFileUploaderDeleteBtn"] button:hover {
    color: #E11D48 !important;
}

/* BaseWeb Select Box Container & Inputs (Eradicate Dark Backgrounds) */
div[data-baseweb="select"] {
    background-color: transparent !important;
}

div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid rgba(14, 165, 233, 0.28) !important;
    border-radius: 12px !important;
    color: #0F172A !important;
    box-shadow: 0 2px 8px rgba(14, 165, 233, 0.04) !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: #0284C7 !important;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.12) !important;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: #0284C7 !important;
    box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.25) !important;
}

/* All text inside select box */
div[data-baseweb="select"] * {
    color: #0F172A !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
}

/* Dropdown Caret Icon */
div[data-baseweb="select"] svg {
    fill: #0284C7 !important;
    color: #0284C7 !important;
}

/* Dropdown Menu Popover / Floating Menu (White & Coastal Palette) */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[role="listbox"],
ul[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
    border: 1px solid rgba(14, 165, 233, 0.25) !important;
    box-shadow: 0 12px 32px rgba(14, 165, 233, 0.16) !important;
}

li[role="option"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    font-size: 0.9rem !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid rgba(14, 165, 233, 0.08) !important;
    transition: all 0.15s ease !important;
}

li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: #F0F9FF !important;
    color: #0284C7 !important;
    font-weight: 600 !important;
}

li[role="option"] * {
    color: inherit !important;
}

/* Input Fields (Zero Dark) */
input[type="text"], input[type="number"], textarea, div[data-baseweb="input"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid rgba(14, 165, 233, 0.28) !important;
    border-radius: 10px !important;
    color: #0F172A !important;
}

input[type="text"]:focus, input[type="number"]:focus, textarea:focus, div[data-baseweb="input"] > div:focus-within {
    border-color: #0284C7 !important;
    box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.2) !important;
}

/* Portrait Viewport Image Styling */
[data-testid="stImage"] {
    background-color: transparent !important;
    border-radius: 14px !important;
}

[data-testid="stImage"] > img {
    border-radius: 14px !important;
    border: 1px solid rgba(14, 165, 233, 0.25) !important;
    box-shadow: 0 4px 18px rgba(14, 165, 233, 0.08) !important;
    background-color: #FFFFFF !important;
}

[data-testid="stImageCaption"] {
    color: #475569 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
}

/* Streamlit Alerts (Clean Seafoam / Aqua) */
[data-testid="stAlert"] {
    background-color: #F0F9FF !important;
    color: #0369A1 !important;
    border: 1px solid rgba(14, 165, 233, 0.3) !important;
    border-radius: 12px !important;
}

[data-testid="stAlert"] * {
    color: #0369A1 !important;
}

/* Streamlit Expanders */
details, [data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1px solid rgba(14, 165, 233, 0.22) !important;
    border-radius: 12px !important;
    color: #0F172A !important;
}

[data-testid="stExpander"] summary {
    color: #0F172A !important;
    font-weight: 600 !important;
}


/* Base App Coastal Water Sea-Blue & Sea-Green Background (NO DARK MODE) */
.stApp {
    background-color: #F8FAFC !important;
    background-image: 
        radial-gradient(ellipse 90% 60% at 50% -10%, rgba(14, 165, 233, 0.16) 0%, rgba(16, 185, 129, 0.09) 45%, #F8FAFC 85%) !important;
    background-attachment: fixed !important;
}

/* Precision Oceanic Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
    background: #0284C7;
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
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.18) 0%, rgba(16, 185, 129, 0.22) 100%);
    border: 1px solid rgba(14, 165, 233, 0.4);
    box-shadow: 0 8px 32px rgba(14, 165, 233, 0.22);
    margin-bottom: 16px;
}

.brand-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.035em;
    color: #0F172A;
    margin-bottom: 0.3rem;
}

.brand-subtitle {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Plus Jakarta Sans", sans-serif;
    font-size: 1.05rem;
    color: #475569;
    margin-bottom: 1.2rem;
    letter-spacing: -0.01em;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.55;
}

/* Flagship Feature Action Cards */
.hero-action-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(14, 165, 233, 0.22);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.85rem;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 16px rgba(14, 165, 233, 0.06);
}
.hero-action-card:hover {
    background: #FFFFFF;
    border-color: rgba(14, 165, 233, 0.45);
    transform: translateY(-2px);
    box-shadow: 0 10px 28px -4px rgba(14, 165, 233, 0.18);
}

/* Glassmorphism Card Container (Sea-Blue & Sea-Green Accent) */
.luxury-card {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(14, 165, 233, 0.2);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 6px 24px -2px rgba(14, 165, 233, 0.08), 0 2px 8px rgba(16, 185, 129, 0.04);
    transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}

.luxury-card:hover {
    border-color: rgba(14, 165, 233, 0.4);
    box-shadow: 0 12px 32px -4px rgba(14, 165, 233, 0.16);
    transform: translateY(-2px);
}

/* KPI Metric Meter Box */
.metric-box {
    background: #FFFFFF;
    border: 1px solid rgba(14, 165, 233, 0.22);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    text-align: left;
    box-shadow: 0 4px 18px rgba(14, 165, 233, 0.07);
}

.metric-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

.metric-val {
    font-size: 1.7rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0284C7;
    line-height: 1.2;
}

.metric-subtitle {
    font-size: 0.78rem;
    color: #475569;
    margin-top: 0.25rem;
}

/* Status Pills */
.pill-badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

.pill-cyan {
    background: rgba(14, 165, 233, 0.12);
    color: #0284C7;
    border: 1px solid rgba(14, 165, 233, 0.35);
}

.pill-emerald {
    background: rgba(16, 185, 129, 0.12);
    color: #059669;
    border: 1px solid rgba(16, 185, 129, 0.35);
}

.pill-violet {
    background: rgba(124, 58, 237, 0.10);
    color: #7C3AED;
    border: 1px solid rgba(124, 58, 237, 0.3);
}

.pill-rose {
    background: rgba(225, 29, 72, 0.10);
    color: #E11D48;
    border: 1px solid rgba(225, 29, 72, 0.3);
}

.pill-amber {
    background: rgba(217, 119, 6, 0.10);
    color: #D97706;
    border: 1px solid rgba(217, 119, 6, 0.3);
}

/* Routine Step Timeline Card */
.routine-step {
    background: #FFFFFF;
    border-left: 4px solid #0284C7;
    border-top: 1px solid rgba(14, 165, 233, 0.18);
    border-right: 1px solid rgba(14, 165, 233, 0.18);
    border-bottom: 1px solid rgba(14, 165, 233, 0.18);
    border-radius: 0 14px 14px 0;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 4px 14px rgba(14, 165, 233, 0.06);
}

.step-num {
    font-size: 0.75rem;
    font-weight: 700;
    color: #0284C7;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.step-compound {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0.15rem 0 0.3rem 0;
}

.step-moa {
    font-size: 0.84rem;
    color: #475569;
    line-height: 1.5;
    margin-bottom: 0.6rem;
}

.search-box {
    background: #F0FDF4;
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 8px;
    padding: 0.45rem 0.75rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.76rem;
    color: #059669;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Completely eliminate sidebar from the page */
[data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}

/* 3D Glass Step Tracker Ribbon */
.step-tracker {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin: 1.5rem auto 2.5rem auto;
    max-width: 760px;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 18px;
    border-radius: 9999px;
    background: #FFFFFF;
    border: 1px solid rgba(14, 165, 233, 0.22);
    box-shadow: 0 2px 8px rgba(14, 165, 233, 0.08);
    transition: all 0.3s ease;
}

.step-item.active {
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(16, 185, 129, 0.12) 100%);
    border-color: #0284C7;
    box-shadow: 0 0 20px rgba(14, 165, 233, 0.25);
}

.step-num-badge {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0284C7 0%, #0D9488 100%);
    color: #FFFFFF;
    font-size: 0.72rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}

.step-name {
    font-size: 0.82rem;
    font-weight: 600;
    color: #0F172A;
    letter-spacing: -0.01em;
}

.step-divider-line {
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, rgba(14, 165, 233, 0.3), rgba(16, 185, 129, 0.3));
    max-width: 40px;
}

/* 3D Luxury Glass Card */
.glass-3d-card {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(14, 165, 233, 0.22);
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 12px 36px -10px rgba(14, 165, 233, 0.14), 0 2px 8px rgba(16, 185, 129, 0.06);
    backdrop-filter: blur(16px);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.glass-3d-card:hover {
    border-color: rgba(14, 165, 233, 0.45);
    box-shadow: 0 18px 45px -10px rgba(14, 165, 233, 0.22), 0 0 24px rgba(16, 185, 129, 0.1);
    transform: translateY(-2px);
}

.section-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #0284C7;
    margin-bottom: 0.5rem;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #0F172A;
    margin-bottom: 0.3rem;
}

.section-desc {
    font-size: 0.9rem;
    color: #475569;
    margin-bottom: 1.2rem;
    line-height: 1.55;
}

/* Sleek Sea-Blue to Sea-Green Button Styling */
.stButton > button {
    background: linear-gradient(135deg, #0284C7 0%, #0D9488 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.94rem !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    padding: 0.7rem 1.8rem !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.35) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0369A1 0%, #0F766E 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(14, 165, 233, 0.45) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Tabs Header */
.stTabs [data-baseweb="tab-list"] {
    gap: 1.5rem;
    border-bottom: 1px solid rgba(14, 165, 233, 0.2);
    padding-bottom: 0.3rem;
}

.stTabs [data-baseweb="tab"] {
    color: #64748B;
    font-weight: 600;
    font-size: 0.92rem;
    padding: 0.5rem 0;
    background-color: transparent !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    color: #0284C7 !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #0284C7 !important;
}

/* Remove default Streamlit top padding & preserve center canvas */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1100px !important;
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

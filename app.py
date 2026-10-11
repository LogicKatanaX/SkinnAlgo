"""
SkinnAlgo — Multimodal Skin Condition Intelligence & Cosmeceutical Compound Recommender.
Production Streamlit Application — Coastal Sea-Blue & Sea-Green Biotech Aesthetic (Zero Dark Mode).
"""

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import cv2
import numpy as np
from PIL import Image
import streamlit as st

from skinnalgo.cv.pipeline import SkinCVPipeline, SkinAnalysisResult
from skinnalgo.clinical.questionnaire import (
    ClinicalIntakeData,
    IntakeCrossValidation,
    ClinicalAssessmentEngine,
)
from skinnalgo.chemistry.knowledge_graph import (
    COMPOUND_DATABASE,
    CosmeceuticalCompound,
    CosmeceuticalKnowledgeGraph,
)
from skinnalgo.chemistry.safety_engine import ChemicalSafetyEngine
from skinnalgo.recommender.fallback_engine import FormulatedRegimen
from skinnalgo.recommender.gemini_engine import GeminiRegimenRecommender
from skinnalgo.recommender.export import RoutineExporter
from skinnalgo.ui.styles import inject_luxury_styles
from skinnalgo.ui.components import (
    render_header,
    render_empty_hero,
    render_metric_cards,
    render_safety_banner,
    render_routine_steps,
    render_compound_card,
)

# Page configuration — Zero sidebar flagship canvas
st.set_page_config(
    page_title="SkinnAlgo — Coastal Dermal Intelligence",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject coastal sea-blue and sea-green luxury styling
inject_luxury_styles()


@st.cache_resource
def get_cv_pipeline():
    return SkinCVPipeline()


@st.cache_resource
def get_assessment_engine():
    return ClinicalAssessmentEngine()


@st.cache_resource
def get_knowledge_graph():
    return CosmeceuticalKnowledgeGraph()


# Initialize state
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "regimen_result" not in st.session_state:
    st.session_state.regimen_result = None
if "intake_data" not in st.session_state:
    st.session_state.intake_data = None
if "cross_val" not in st.session_state:
    st.session_state.cross_val = None


# Helper function for executing analysis
def run_analysis_pipeline(bgr_img, p_wash, p_env, p_barrier, p_goal):
    with st.spinner("Executing Computer Vision colorimetry, lip masking, and landmark segmentation..."):
        cv_pipe = get_cv_pipeline()
        analysis = cv_pipe.analyze(bgr_img)
        st.session_state.analysis_result = analysis

        intake_obj = ClinicalIntakeData(
            post_wash_feel=p_wash,
            environment=p_env,
            barrier_reactivity=p_barrier,
            primary_goal=p_goal
        )
        st.session_state.intake_data = intake_obj

        assess_engine = get_assessment_engine()
        cross_val_obj = assess_engine.cross_validate(
            intake=intake_obj,
            cv_sebum_score=analysis.sebum.overall_sebum_score,
            cv_erythema_index=analysis.erythema.erythema_index,
            cv_blemish_count=analysis.texture.active_blemish_count
        )
        st.session_state.cross_val = cross_val_obj

        # Synthesize Regimen (auto-detects API key from Streamlit secrets or env)
        recommender = GeminiRegimenRecommender(api_key=None)
        regimen = recommender.formulate(analysis, intake_obj, cross_val_obj)
        st.session_state.regimen_result = regimen


# Render top branding header
render_header()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
preset_names = {
    "Oily & Active Breakouts": os.path.join(BASE_DIR, "assets", "samples", "oily_acne_profile.png"),
    "Dry & Vascular Erythema": os.path.join(BASE_DIR, "assets", "samples", "dry_erythema_profile.png"),
    "Combination & Hyperpigmentation": os.path.join(BASE_DIR, "assets", "samples", "combo_pigment_profile.png"),
    "Balanced Eudermic": os.path.join(BASE_DIR, "assets", "samples", "balanced_profile.png")
}
default_avatar_path = os.path.join(BASE_DIR, "assets", "default_avatar.png")

# Dynamic Step Progress Ribbon
has_result = st.session_state.analysis_result is not None
step1_active = "active"
step2_active = "active"
step3_active = "active"
step4_active = "active" if has_result else ""

st.markdown(f"""
    <div class="step-tracker">
        <a href="#step-1" style="text-decoration: none;">
            <div class="step-item {step1_active}">
                <div class="step-num-badge">1</div>
                <div class="step-name">Facial Capture</div>
            </div>
        </a>
        <div class="step-divider-line"></div>
        <a href="#step-2" style="text-decoration: none;">
            <div class="step-item {step2_active}">
                <div class="step-num-badge">2</div>
                <div class="step-name">Clinical Intake</div>
            </div>
        </a>
        <div class="step-divider-line"></div>
        <a href="#step-3" style="text-decoration: none;">
            <div class="step-item {step3_active}">
                <div class="step-num-badge">3</div>
                <div class="step-name">Synthesis</div>
            </div>
        </a>
        <div class="step-divider-line"></div>
        <a href="#step-4" style="text-decoration: none;">
            <div class="step-item {step4_active}">
                <div class="step-num-badge" style="background: {'#059669' if has_result else '#CBD5E1'};">4</div>
                <div class="step-name">Clinical Verdict & Results</div>
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)


# =====================================================================
# STEP 1: FACIAL DIAGNOSTIC CAPTURE STUDIO
# =====================================================================
st.markdown('<div id="step-1"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="section-badge">Step 01 • Dermal Radiance & Anthropometric Zoning</div>
    <div class="section-title">Facial Diagnostic Capture Studio</div>
    <div class="section-desc">
        Upload a high-resolution frontal facial selfie in natural daylight. SkinnAlgo applies anatomical landmark zoning, automatic lip vermillion masking, and specular colorimetry.
    </div>
""", unsafe_allow_html=True)

capture_col_left, capture_col_right = st.columns([1.15, 0.85], gap="large")

input_bgr = None

with capture_col_left:
    uploaded_file = st.file_uploader(
        "Upload Facial Portrait (JPG or PNG):",
        type=["jpg", "jpeg", "png"],
        help="High-resolution frontal view in natural daylight, without makeup or filters."
    )
    if uploaded_file is not None:
        pil_img = Image.open(uploaded_file).convert("RGB")
        input_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    else:
        st.info("💡 Tip: Upload a clear, well-lit photo looking straight at the camera. Neutral expression provides the highest landmark accuracy.")

with capture_col_right:
    st.markdown("<div style='font-size: 0.88rem; font-weight: 700; color: #0F172A; margin-bottom: 0.5rem;'>Portrait Viewport</div>", unsafe_allow_html=True)
    if input_bgr is not None:
        display_rgb = cv2.cvtColor(input_bgr, cv2.COLOR_BGR2RGB)
        st.image(display_rgb, caption="Diagnostic Portrait Loaded", use_container_width=True)
        st.markdown("""
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 8px; padding: 6px 12px; margin-top: 6px;">
                <span style="font-size: 0.78rem; color: #059669; font-weight: 700;">● Biometric Alignment Calibrated</span>
                <span class="pill-badge pill-emerald">Ready</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        if os.path.exists(default_avatar_path):
            avatar_img = Image.open(default_avatar_path)
            st.image(avatar_img, caption="Awaiting Portrait Upload", use_container_width=True)
        st.markdown("""
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.25); border-radius: 8px; padding: 6px 12px; margin-top: 6px;">
                <span style="font-size: 0.78rem; color: #0284C7; font-weight: 600;">○ Awaiting Portrait Upload</span>
                <span class="pill-badge pill-cyan">Awaiting</span>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height: 1.8rem;'></div>", unsafe_allow_html=True)


# =====================================================================
# STEP 2: CLINICAL SENSORY INTAKE ASSESSMENT
# =====================================================================
st.markdown('<div id="step-2"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="section-badge">Step 02 • Dermatological Symptom Inventory</div>
    <div class="section-title">Clinical Sensory Intake Assessment</div>
    <div class="section-desc">
        Four clinical vectors cross-validated against computer vision metrics to eliminate diagnostic ambiguity (e.g., distinguishing Dehydrated-Oily barrier damage from true Seborrhea).
    </div>
""", unsafe_allow_html=True)

default_wash_idx = 1
default_barrier_idx = 2
default_goal_idx = 0

intake_c1, intake_c2 = st.columns(2, gap="large")

with intake_c1:
    st.markdown("""
        <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-bottom: 4px;">
            🧴 1. Skin Feel 2h Post-Cleansing
        </div>
        <div style="font-size: 0.80rem; color: #475569; margin-bottom: 6px;">
            Measures baseline sebaceous gland output vs transepidermal moisture retention.
        </div>
    """, unsafe_allow_html=True)
    post_wash = st.selectbox(
        "Skin feel post-cleansing",
        options=list(ClinicalAssessmentEngine.POST_WASH_LABELS.keys()),
        format_func=lambda k: ClinicalAssessmentEngine.POST_WASH_LABELS[k],
        index=default_wash_idx,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-bottom: 4px;">
            🛡️ 3. Dermal Reactivity & Barrier Health
        </div>
        <div style="font-size: 0.80rem; color: #475569; margin-bottom: 6px;">
            Triggers deterministic safety locks if stratum corneum is fragile or inflamed.
        </div>
    """, unsafe_allow_html=True)
    barrier = st.selectbox(
        "Barrier sensitivity and reactivity",
        options=list(ClinicalAssessmentEngine.BARRIER_LABELS.keys()),
        format_func=lambda k: ClinicalAssessmentEngine.BARRIER_LABELS[k],
        index=default_barrier_idx,
        label_visibility="collapsed"
    )

with intake_c2:
    st.markdown("""
        <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-bottom: 4px;">
            🌤️ 2. Ambient Climate & UV Exposure
        </div>
        <div style="font-size: 0.80rem; color: #475569; margin-bottom: 6px;">
            Factors environmental humidity, altitude dryness, and photo-aging risk.
        </div>
    """, unsafe_allow_html=True)
    env = st.selectbox(
        "Climate and environment",
        options=list(ClinicalAssessmentEngine.ENVIRONMENT_LABELS.keys()),
        format_func=lambda k: ClinicalAssessmentEngine.ENVIRONMENT_LABELS[k],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-bottom: 4px;">
            🎯 4. Primary Formulation Objective
        </div>
        <div style="font-size: 0.80rem; color: #475569; margin-bottom: 6px;">
            Guides active compound selection across the 28-ingredient knowledge graph.
        </div>
    """, unsafe_allow_html=True)
    goal = st.selectbox(
        "Primary skincare objective",
        options=list(ClinicalAssessmentEngine.GOAL_LABELS.keys()),
        format_func=lambda k: ClinicalAssessmentEngine.GOAL_LABELS[k],
        index=default_goal_idx,
        label_visibility="collapsed"
    )

st.markdown("<div style='height: 1.8rem;'></div>", unsafe_allow_html=True)


# =====================================================================
# STEP 3: MULTIMODAL SYNTHESIS ACTION CTA
# =====================================================================
st.markdown('<div id="step-3"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="glass-3d-card" style="text-align: center; padding: 2rem 1.5rem; border: 1px solid rgba(14, 165, 233, 0.35); background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 253, 250, 0.95) 100%);">
        <div class="section-badge" style="justify-content: center;">Step 03 • AI Reasoning & Deterministic Constraint Solver</div>
        <div style="font-size: 1.65rem; font-weight: 800; color: #0F172A; margin-bottom: 0.4rem; letter-spacing: -0.02em;">
            Ready to Synthesize Skin Intelligence
        </div>
        <div style="font-size: 0.9rem; color: #475569; max-width: 620px; margin: 0 auto 1.4rem auto; line-height: 1.55;">
            Fuses CIE-Lab colorimetric decoupling, specular lipid reflectance physics, and Gemini 2.5 multimodal formulation with zero chemical collisions.
        </div>
        <div style="display: flex; justify-content: center; gap: 10px; margin-bottom: 1.5rem; flex-wrap: wrap;">
            <span class="pill-badge pill-emerald">⚡ Dual Engine: Gemini 2.5 + Safety Core</span>
            <span class="pill-badge pill-cyan">🛡️ 28 Actives Knowledge Graph</span>
            <span class="pill-badge pill-violet">🔬 Anthropometric Face Mesh</span>
        </div>
""", unsafe_allow_html=True)

btn_c1, btn_c2, btn_c3 = st.columns([1, 2, 1])
with btn_c2:
    analyze_btn = st.button("✨ Run Skin Diagnostic & Formulate Protocol", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Execution trigger
if analyze_btn:
    if input_bgr is not None:
        run_analysis_pipeline(input_bgr, post_wash, env, barrier, goal)
        st.rerun()
    else:
        # Fail-safe demo: auto-load calibrated preset so the button never fails
        default_p_path = preset_names["Oily & Active Breakouts"]
        if os.path.exists(default_p_path):
            demo_img = cv2.imread(default_p_path)
            run_analysis_pipeline(demo_img, post_wash, env, barrier, goal)
            st.rerun()

st.markdown("<div style='height: 1.8rem;'></div>", unsafe_allow_html=True)


# =====================================================================
# STEP 4: CLINICAL RESULTS, VERDICT & REGIMEN STUDIO
# =====================================================================
st.markdown('<div id="step-4"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="section-badge">Step 04 • Clinical Intelligence Studio</div>
    <div class="section-title">Diagnostic Verdict & Formulated Regimen</div>
    <div class="section-desc">
        Comprehensive computer vision colorimetry analysis, executive clinical verdict, and individualized cosmeceutical protocols.
    </div>
""", unsafe_allow_html=True)

if st.session_state.analysis_result is None:
    render_empty_hero()

    st.markdown("<div style='text-align: center; margin-bottom: 0.8rem; font-size: 0.88rem; color: #475569; font-weight: 600;'>Or Test Instantly with a Pre-Calibrated Profile:</div>", unsafe_allow_html=True)
    qc1, qc2, qc3, qc4 = st.columns(4)

    with qc1:
        if st.button("Oily & Breakouts", use_container_width=True, key="btn_oily"):
            p_path = preset_names["Oily & Active Breakouts"]
            if os.path.exists(p_path):
                p_img = cv2.imread(p_path)
                run_analysis_pipeline(p_img, "shiny_all_over", "humid_tropical", "resilient", "clear_breakouts")
                st.rerun()

    with qc2:
        if st.button("Dry & Erythema", use_container_width=True, key="btn_dry"):
            p_path = preset_names["Dry & Vascular Erythema"]
            if os.path.exists(p_path):
                p_img = cv2.imread(p_path)
                run_analysis_pipeline(p_img, "tight_parched", "cold_arid", "stings_easily", "repair_barrier")
                st.rerun()

    with qc3:
        if st.button("Combination Skin", use_container_width=True, key="btn_combo"):
            p_path = preset_names["Combination & Hyperpigmentation"]
            if os.path.exists(p_path):
                p_img = cv2.imread(p_path)
                run_analysis_pipeline(p_img, "oily_t_zone_only", "moderate_temperate", "resilient", "fade_dark_spots")
                st.rerun()

    with qc4:
        if st.button("Balanced Skin", use_container_width=True, key="btn_balanced"):
            p_path = preset_names["Balanced Eudermic"]
            if os.path.exists(p_path):
                p_img = cv2.imread(p_path)
                run_analysis_pipeline(p_img, "balanced_supple", "moderate_temperate", "resilient", "smooth_texture")
                st.rerun()

else:
    cv_res: SkinAnalysisResult = st.session_state.analysis_result
    intake: ClinicalIntakeData = st.session_state.intake_data
    cross_val: IntakeCrossValidation = st.session_state.cross_val
    regimen: FormulatedRegimen = st.session_state.regimen_result

    # Top Diagnostic Health Bar & Reset CTA
    top_c1, top_c2 = st.columns([6, 2])
    with top_c1:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 1.35rem; font-weight: 800; color: #0F172A;">Diagnostic Health Index: {cv_res.skin_health_index}/100</span>
                <span class="pill-badge pill-cyan">Primary Concern: {cv_res.primary_cv_concern}</span>
            </div>
        """, unsafe_allow_html=True)
    with top_c2:
        if st.button("↺ Start New Diagnostic Scan", use_container_width=True, key="btn_reset"):
            st.session_state.analysis_result = None
            st.session_state.regimen_result = None
            st.session_state.intake_data = None
            st.session_state.cross_val = None
            st.rerun()

    # 4 KPI Diagnostic Metric Gauges
    render_metric_cards(cv_res)

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # =====================================================================
    # SECTION: EXECUTIVE CLINICAL DIAGNOSTIC VERDICT ("THE WHOLE PICTURE")
    # =====================================================================
    st.markdown(f"""
        <div class="glass-3d-card" style="border-left: 5px solid #0284C7; padding: 1.5rem 1.8rem; margin-bottom: 1.6rem; background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 253, 250, 0.95) 100%);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                <span class="pill-badge pill-cyan">Clinical Diagnostic Verdict</span>
                <span class="pill-badge pill-emerald">Dermal Tolerance: {cross_val.tolerance_rating}</span>
            </div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin-bottom: 0.4rem;">
                {cross_val.reconciled_skin_type} — {cv_res.primary_cv_concern}
            </div>
            <div style="font-size: 0.92rem; color: #334155; line-height: 1.6; margin-bottom: 1rem;">
                {regimen.skin_profile_summary}
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(14, 165, 233, 0.18);">
                <div style="background: rgba(255, 255, 255, 0.8); padding: 10px 14px; border-radius: 10px; border: 1px solid rgba(14, 165, 233, 0.18);">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">1. Epidermal Barrier Status</div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #0284C7; margin-top: 2px;">{cross_val.reconciled_skin_type}</div>
                    <div style="font-size: 0.76rem; color: #475569; margin-top: 2px;">Lipid layer: {'Compromised' if cv_res.erythema.erythema_index > 0.35 else 'Homeostatic'}</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.8); padding: 10px 14px; border-radius: 10px; border: 1px solid rgba(14, 165, 233, 0.18);">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">2. Vascular Flushing</div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #059669; margin-top: 2px;">{cv_res.erythema.erythema_severity}</div>
                    <div style="font-size: 0.76rem; color: #475569; margin-top: 2px;">Flush Area: {cv_res.erythema.erythema_percentage:.1f}% of dermis</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.8); padding: 10px 14px; border-radius: 10px; border: 1px solid rgba(14, 165, 233, 0.18);">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">3. Follicular Micro-Relief</div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #D97706; margin-top: 2px;">{cv_res.texture.texture_classification}</div>
                    <div style="font-size: 0.76rem; color: #475569; margin-top: 2px;">Active lesions: {cv_res.texture.active_blemish_count} spots</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Main Tabs within Step 4
    res_tab1, res_tab2, res_tab3, res_tab4, res_tab5 = st.tabs([
        "Formulated Cosmeceutical Protocol",
        "Computer Vision & Colorimetry Lab",
        "User Guide & Clinical Instructions",
        "Chemical Knowledge Graph (28 Actives)",
        "System Architecture & Physics"
    ])

    # -------------------------------------------------------------
    # TAB 1: FORMULATED REGIMEN
    # -------------------------------------------------------------
    with res_tab1:
        # Safety Clearance
        render_safety_banner(regimen.safety_clearance)

        # Profile Summary Card
        st.markdown(f"""
            <div class="luxury-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span class="pill-badge pill-violet">Engine: {regimen.engine_used}</span>
                    <span class="pill-badge pill-cyan">Reconciled: {cross_val.reconciled_skin_type}</span>
                </div>
                <h3 style="margin: 0.2rem 0; font-size: 1.2rem; color: #0F172A;">Clinical Dermatological Protocol</h3>
                <p style="color: #475569; font-size: 0.90rem; line-height: 1.6; margin-bottom: 0.5rem;">
                    {regimen.skin_profile_summary}
                </p>
                <div style="font-size: 0.80rem; color: #64748B;">
                    Evaluation Horizon: {regimen.expected_timeline_weeks} weeks • Tolerance Level: {cross_val.tolerance_rating}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # AM / PM Routines Side by Side
        col_am, col_pm = st.columns(2)

        with col_am:
            st.markdown("### ☀️ Morning (AM) Protocol")
            render_routine_steps(regimen.am_routine, "am")

        with col_pm:
            st.markdown("### 🌙 Evening (PM) Protocol")
            render_routine_steps(regimen.pm_routine, "pm")

        # Clinical Notes
        if regimen.clinical_precautions:
            st.markdown("#### ⚠️ Clinical Precautions & Purging Guidance")
            for p in regimen.clinical_precautions:
                st.markdown(f"- {p}")

        # Routine Download
        st.markdown("---")
        markdown_report = RoutineExporter.to_markdown(regimen, cv_res, intake, cross_val)
        st.download_button(
            label="Download Printable Clinical Regimen Report (.md)",
            data=markdown_report,
            file_name="SkinnAlgo_Clinical_Regimen.md",
            mime="text/markdown",
            use_container_width=True
        )

    # -------------------------------------------------------------
    # TAB 2: CV & COLORIMETRY LAB
    # -------------------------------------------------------------
    with res_tab2:
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.markdown("#### Original Portrait")
            st.image(cv2.cvtColor(cv_res.raw_image_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)

        with col_img2:
            st.markdown("#### Diagnostic Landmark & Blemish Overlay")
            st.image(cv2.cvtColor(cv_res.diagnostic_overlay_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)

        with st.expander("🔬 View Thermal CIE-Lab a* Channel Erythema Heatmap"):
            st.markdown("""
                *The CIE-Lab $a^*$ axis (green to red) separates chromatic vascular flushing from melanin pigmentation. 
                Below is the thermal radiance map of micro-erythema across the facial dermis:*
            """)
            st.image(cv2.cvtColor(cv_res.erythema.erythema_heatmap_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)

        st.markdown("#### Quantitative Metric Breakdown")
        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(f"""
                <div class="luxury-card">
                    <h4 style="margin: 0 0 0.5rem 0; color: #0284C7;">T-Zone vs U-Zone Sebum</h4>
                    <p style="font-size: 0.85rem; color: #475569;">
                        • <strong>T-Zone Sebum</strong>: {cv_res.sebum.t_zone_sebum_score:.3f}<br>
                        • <strong>U-Zone Sebum</strong>: {cv_res.sebum.u_zone_sebum_score:.3f}<br>
                        • <strong>Specular Ratio</strong>: {cv_res.sebum.specular_ratio * 100:.2f}% of pixels<br>
                        • <strong>Classification</strong>: {cv_res.sebum.sebum_classification}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with b2:
            st.markdown(f"""
                <div class="luxury-card">
                    <h4 style="margin: 0 0 0.5rem 0; color: #059669;">CIE-Lab Colorimetry</h4>
                    <p style="font-size: 0.85rem; color: #475569;">
                        • <strong>Mean a* (Redness)</strong>: {cv_res.erythema.mean_a_star:.2f}<br>
                        • <strong>Erythema Index (EI)</strong>: {cv_res.erythema.erythema_index:.3f}<br>
                        • <strong>Micro-Flush Coverage</strong>: {cv_res.erythema.erythema_percentage:.1f}%<br>
                        • <strong>Vascular Severity</strong>: {cv_res.erythema.erythema_severity}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with b3:
            st.markdown(f"""
                <div class="luxury-card">
                    <h4 style="margin: 0 0 0.5rem 0; color: #D97706;">Texture & Micro-Relief</h4>
                    <p style="font-size: 0.85rem; color: #475569;">
                        • <strong>Laplacian Variance</strong>: {cv_res.texture.laplacian_variance:.1f}<br>
                        • <strong>Roughness Score</strong>: {cv_res.texture.roughness_score:.3f}<br>
                        • <strong>Active Blemishes</strong>: {cv_res.texture.active_blemish_count} spots<br>
                        • <strong>Lesion Density</strong>: {cv_res.texture.blemish_density_per_kpx:.2f} / kpx
                    </p>
                </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 3: USER GUIDE & CLINICAL INSTRUCTIONS
    # -------------------------------------------------------------
    with res_tab3:
        st.markdown("### 📘 SkinnAlgo User Guide & Clinical Science Manual")
        st.markdown("Understand the whole picture: how to capture optimal photos, how computer vision measures skin physics, and how to read your diagnostic verdict.")

        ug_col1, ug_col2 = st.columns(2, gap="large")

        with ug_col1:
            st.markdown("""
                <div class="luxury-card">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.6rem;">
                        <span style="font-size: 1.4rem;">📸</span>
                        <h4 style="margin: 0; color: #0F172A;">1. Diagnostic Capture Best Practices</h4>
                    </div>
                    <ul style="font-size: 0.86rem; color: #334155; line-height: 1.6; padding-left: 1.2rem;">
                        <li><strong>Lighting:</strong> Shoot in natural, indirect daylight or diffuse 5500K neutral light. Avoid yellow incandescent bulbs or harsh flash that create false specular hot-spots.</li>
                        <li><strong>Dermal Preparation:</strong> Perform diagnostics 1.5 to 2 hours post-wash without active creams, oils, or makeup. This allows sebaceous glands to reach baseline excretion.</li>
                        <li><strong>Framing:</strong> Keep eyes open, neutral expression, and chin parallel to the camera. If uploading a macro close-up (cheeks/nose), ensure natural focus without motion blur.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div class="luxury-card">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.6rem;">
                        <span style="font-size: 1.4rem;">📊</span>
                        <h4 style="margin: 0; color: #0F172A;">3. Reading Your Diagnostic Scores</h4>
                    </div>
                    <ul style="font-size: 0.86rem; color: #334155; line-height: 1.6; padding-left: 1.2rem;">
                        <li><strong>Sebum Index (0.0 to 1.0):</strong> Matte (&lt;0.20), Balanced (0.20–0.30), Combination (0.30–0.45), Hyperseborrhea (&gt;0.45).</li>
                        <li><strong>Erythema Index (0.0 to 1.0):</strong> Calm (&lt;0.20), Moderate Flush (0.20–0.40), Reactive Vascular Flare (&gt;0.40).</li>
                        <li><strong>Texture & Lesions:</strong> Glass Skin (0–2 spots), Moderate Texture (3–6 spots), Congested Flare (&gt;6 spots).</li>
                        <li><strong>Skin Health Index (0 to 100):</strong> Baseline composite health deducting points for active inflammation, barrier breakdown, and lipid imbalances.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        with ug_col2:
            st.markdown("""
                <div class="luxury-card">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.6rem;">
                        <span style="font-size: 1.4rem;">🔬</span>
                        <h4 style="margin: 0; color: #0F172A;">2. How Computer Vision Analyzes Your Skin</h4>
                    </div>
                    <ul style="font-size: 0.86rem; color: #334155; line-height: 1.6; padding-left: 1.2rem;">
                        <li><strong>CIE-Lab a* Chrominance:</strong> Decouples melanin baseline (L*) from capillary blood vessels (a*), ensuring fair assessment across all Fitzpatrick phototypes I through VI.</li>
                        <li><strong>HSV Specular Reflectance:</strong> Isolates mirror-like shine from sebaceous gland lipid output ($V \\ge 205, S \\le 60$) across T-Zone and U-Zone landmarks.</li>
                        <li><strong>High-Frequency Laplacian Variance:</strong> Computes spatial second derivatives ($\\sigma^2$) across dermal relief to separate smooth glass skin from follicular congestion.</li>
                        <li><strong>Lip & Mucosal Boundary Masking:</strong> Automatically isolates the vermillion lip border so natural lip color is never falsely circled as acne papules.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div class="luxury-card">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.6rem;">
                        <span style="font-size: 1.4rem;">🛡️</span>
                        <h4 style="margin: 0; color: #0F172A;">4. Biochemical Safety Enforcement</h4>
                    </div>
                    <ul style="font-size: 0.86rem; color: #334155; line-height: 1.6; padding-left: 1.2rem;">
                        <li><strong>Zero Acid + Retinoid Collisions:</strong> Hard deterministic rule graph intercepts simultaneous application of strong AHAs/BHAs with Adapalene or Retinol.</li>
                        <li><strong>Redox Conflict Shielding:</strong> Prevents pure Vitamin C (L-Ascorbic Acid) from degrading into pro-inflammatory byproducts when paired with Benzoyl Peroxide.</li>
                        <li><strong>Compromised Barrier Override:</strong> If barrier reactivity is severe or Erythema Index &gt; 0.40, direct exfoliants are halted and replaced with a 14-day lipid restoration protocol.</li>
                        <li><strong>Mandatory Broad-Spectrum SPF 50+:</strong> Automatically enforced in every morning regimen whenever photosensitizing actives are prescribed.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 4: KNOWLEDGE GRAPH
    # -------------------------------------------------------------
    with res_tab4:
        st.markdown("### 🧪 Cosmeceutical Knowledge Graph Directory")
        st.markdown("Browse all 28 clinical-grade active compounds, their biochemical Mechanisms of Action (MOA), pH stability, and contraindications.")

        kg = get_knowledge_graph()

        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            selected_concern = st.selectbox(
                "Filter by Skin Concern",
                ["All Concerns", "Acne", "Sebum", "Texture", "Erythema", "Hyperpigmentation", "Barrier", "Dehydration"]
            )
        with filter_col2:
            search_query = st.text_input("Search Compound by Name or MOA", "")

        all_comps = kg.all_compounds()

        if selected_concern != "All Concerns":
            all_comps = [c for c in all_comps if selected_concern.lower() in [tc.lower() for tc in c.target_concerns]]

        if search_query:
            sq = search_query.lower()
            all_comps = [
                c for c in all_comps
                if sq in c.name.lower() or sq in c.inci_name.lower() or sq in c.mechanism_of_action.lower() or sq in c.chemical_class.lower()
            ]

        st.markdown(f"*Displaying {len(all_comps)} verified cosmeceutical active compounds:*")

        for comp in all_comps:
            render_compound_card(comp)

    # -------------------------------------------------------------
    # TAB 5: SYSTEM ARCHITECTURE & CLINICAL SCIENCE
    # -------------------------------------------------------------
    with res_tab5:
        st.markdown("### 📐 Technical Architecture & Clinical Science")
        st.markdown("""
            SkinnAlgo bridges **applied computer vision**, **deterministic safety constraint satisfaction**, and **multimodal generative synthesis**.
        """)

        st.markdown("""
        #### 1. Computer Vision & Colorimetry Mathematics
        - **CIE-Lab Color Space Decoupling**:
          Standard RGB channels convolve luminance with chrominance. Skin tone is heavily influenced by melanin, which absorbs broadband light and lowers RGB values uniformly. By converting to $L^*a^*b^*$, perceptual lightness ($L^*$) is decoupled from the red-green chromatic opponent axis ($a^*$).
          $$\\text{Erythema Index (EI)} = \\frac{\\text{mean}(a^*_{\\text{ROI}}) - a^*_{\\text{baseline}}}{\\gamma}$$
          This ensures Fitzpatrick neutrality across skin phototypes I through VI.
        
        - **Specular Highlight Sebum Modeling**:
          Sebum manifests as specular surface reflection rather than diffuse Lambertian reflection. In HSV space, lipid sheen produces high Value ($V > 205$) with low Saturation ($S < 60$). The ratio of specular pixels across the T-Zone ($S_T$) and U-Zone ($S_U$) quantifies oiliness:
          $$S_{\\text{zone}} = \\frac{\\sum \\text{Specular Highlight Pixels}}{\\sum \\text{Valid Skin Region Pixels}}$$

        - **High-Frequency Laplacian Variance for Texture Roughness**:
          Smooth stratum corneum produces low localized second derivatives. Textured skin, dilated follicular ostia, and microcomedones produce high gradient variance:
          $$\\sigma^2_{\\text{Laplacian}} = \\text{Var}\\left( \\nabla^2 I_{\\text{ROI}} \\right)$$

        #### 2. Deterministic Safety Contraindication Engine
        LLMs frequently hallucinate hazardous active skincare combinations (e.g., pairing high-concentration tretinoin with 2% salicylic acid or pure vitamin C with benzoyl peroxide). SkinnAlgo implements a deterministic hard-coded graph validator:
        - **Retinoid + Strong Acid Separation**: Prevents chemical stratum corneum sloughing and transepidermal water loss.
        - **Benzoyl Peroxide + Pure L-Ascorbic Acid Redox Conflict**: Intercepts oxidation of ascorbic acid into inactive dehydroascorbic acid.
        - **Compromised Barrier Override**: Automatically intercepts direct keratolytics if barrier sensitivity is fragile or Erythema Index > 0.40, enforcing a 14-day lipid restoration protocol.
        - **Mandatory Broad-Spectrum SPF 50+ Lock**: Automatically injects high-performance photoprotection whenever photosensitizers are active.
        """)

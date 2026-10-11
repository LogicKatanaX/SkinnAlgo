"""
SkinnAlgo — Multimodal Skin Condition Intelligence & Cosmeceutical Compound Recommender.
Production Streamlit Application.
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

# Page configuration
st.set_page_config(
    page_title="SkinnAlgo — Multimodal Skin Condition Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject luxury dark styling
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
    with st.spinner("Executing Computer Vision colorimetry and landmark segmentation..."):
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


# Render branding header
render_header()

preset_names = {
    "Oily & Active Breakouts": "assets/samples/oily_acne_profile.png",
    "Dry & Vascular Erythema": "assets/samples/dry_erythema_profile.png",
    "Combination & Hyperpigmentation": "assets/samples/combo_pigment_profile.png",
    "Balanced Eudermic": "assets/samples/balanced_profile.png"
}

# Sidebar: Intake and Image Selector
with st.sidebar:
    st.markdown("### Facial Portrait & Intake")
    
    # Image Input Option (Default to Upload Portrait)
    img_mode = st.radio(
        "Portrait Source",
        ["Upload Portrait", "Clinical Presets", "Webcam Capture"],
        index=0
    )

    input_bgr = None
    default_avatar_path = "assets/default_avatar.png"

    if img_mode == "Upload Portrait":
        uploaded_file = st.file_uploader("Select Portrait Image", type=["jpg", "jpeg", "png"], help="High-resolution frontal view in natural lighting.")
        if uploaded_file is not None:
            pil_img = Image.open(uploaded_file).convert("RGB")
            input_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            st.image(pil_img, caption="Loaded Facial Portrait", use_container_width=True)
        else:
            if os.path.exists(default_avatar_path):
                st.image(default_avatar_path, caption="Awaiting Portrait Upload", use_container_width=True)

    elif img_mode == "Clinical Presets":
        chosen_preset = st.selectbox(
            "Select Calibrated Profile",
            list(preset_names.keys()),
            index=0
        )
        sample_path = preset_names[chosen_preset]
        if os.path.exists(sample_path):
            input_bgr = cv2.imread(sample_path)
            st.image(cv2.cvtColor(input_bgr, cv2.COLOR_BGR2RGB), caption=f"Profile: {chosen_preset}", use_container_width=True)

    elif img_mode == "Webcam Capture":
        cam_file = st.camera_input("Capture Live Portrait")
        if cam_file is not None:
            pil_img = Image.open(cam_file).convert("RGB")
            input_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    st.markdown("---")
    st.markdown("### Clinical Assessment")

    post_wash = st.selectbox(
        "1. Skin feel 2h post-cleansing:",
        options=list(ClinicalAssessmentEngine.POST_WASH_LABELS.keys()),
        format_func=lambda k: ClinicalAssessmentEngine.POST_WASH_LABELS[k],
        index=2 if img_mode == "Clinical Presets" and "Oily" in chosen_preset else (
            0 if img_mode == "Clinical Presets" and "Dry" in chosen_preset else (
                3 if img_mode == "Clinical Presets" and "Combination" in chosen_preset else 1
            )
        )
    )

    env = st.selectbox(
        "2. Climate & Environment:",
        options=list(ClinicalAssessmentEngine.ENVIRONMENT_LABELS.keys()),
        format_func=lambda k: ClinicalAssessmentEngine.ENVIRONMENT_LABELS[k],
        index=0
    )

    barrier = st.selectbox(
        "3. Barrier Sensitivity / Reactivity:",
        options=list(ClinicalAssessmentEngine.BARRIER_LABELS.keys()),
        format_func=lambda k: ClinicalAssessmentEngine.BARRIER_LABELS[k],
        index=0 if img_mode == "Clinical Presets" and "Dry" in chosen_preset else 2
    )

    goal = st.selectbox(
        "4. Primary Skincare Objective:",
        options=list(ClinicalAssessmentEngine.GOAL_LABELS.keys()),
        format_func=lambda k: ClinicalAssessmentEngine.GOAL_LABELS[k],
        index=0 if img_mode == "Clinical Presets" and "Oily" in chosen_preset else (
            2 if img_mode == "Clinical Presets" and "Dry" in chosen_preset else (
                1 if img_mode == "Clinical Presets" and "Combination" in chosen_preset else 3
            )
        )
    )

    st.markdown("---")
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.9rem;">
            <span style="font-size: 0.74rem; color: #64748B; text-transform: uppercase; font-weight: 600; letter-spacing: 0.06em;">Synthesis Engine</span>
            <span class="pill-badge pill-emerald">Dual Engine Ready</span>
        </div>
    """, unsafe_allow_html=True)

    analyze_btn = st.button("Run Skin Diagnostic", use_container_width=True)


# Processing trigger from sidebar button
if analyze_btn:
    if input_bgr is not None:
        run_analysis_pipeline(input_bgr, post_wash, env, barrier, goal)
        st.rerun()
    else:
        st.sidebar.warning("Please upload a portrait or select a preset before analyzing.")


# Main View Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Computer Vision & Colorimetry Lab",
    "Formulated Cosmeceutical Regimen",
    "Chemical Knowledge Graph (28 Actives)",
    "System Architecture & Clinical Science"
])


# =====================================================================
# TAB 1: COMPUTER VISION & COLORIMETRY LAB
# =====================================================================
with tab1:
    if st.session_state.analysis_result is None:
        render_empty_hero()

        st.markdown("<div style='text-align: center; margin-bottom: 0.8rem; font-size: 0.85rem; color: #64748B; font-weight: 500;'>Or test immediately with a calibrated clinical profile:</div>", unsafe_allow_html=True)
        qc1, qc2, qc3, qc4 = st.columns(4)

        with qc1:
            if st.button("Oily & Breakouts", use_container_width=True, key="qc_oily"):
                p_img = cv2.imread(preset_names["Oily & Active Breakouts"])
                run_analysis_pipeline(p_img, "shiny_all_over", "humid_tropical", "resilient", "clear_breakouts")
                st.rerun()

        with qc2:
            if st.button("Dry & Erythema", use_container_width=True, key="qc_dry"):
                p_img = cv2.imread(preset_names["Dry & Vascular Erythema"])
                run_analysis_pipeline(p_img, "tight_parched", "cold_arid", "stings_easily", "repair_barrier")
                st.rerun()

        with qc3:
            if st.button("Combination Skin", use_container_width=True, key="qc_combo"):
                p_img = cv2.imread(preset_names["Combination & Hyperpigmentation"])
                run_analysis_pipeline(p_img, "oily_t_zone_only", "moderate_temperate", "resilient", "fade_dark_spots")
                st.rerun()

        with qc4:
            if st.button("Balanced Skin", use_container_width=True, key="qc_balanced"):
                p_img = cv2.imread(preset_names["Balanced Eudermic"])
                run_analysis_pipeline(p_img, "balanced_supple", "moderate_temperate", "resilient", "smooth_texture")
                st.rerun()

    else:
        cv_res: SkinAnalysisResult = st.session_state.analysis_result

        # Metric Gauges
        render_metric_cards(cv_res)

        st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.markdown("#### Original Portrait")
            st.image(cv2.cvtColor(cv_res.raw_image_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)

        with col_img2:
            st.markdown("#### Diagnostic Landmark & Blemish Overlay")
            st.image(cv2.cvtColor(cv_res.diagnostic_overlay_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)

        # Thermal CIE-Lab Redness Heatmap Toggle
        with st.expander("🔬 View Thermal CIE-Lab a* Channel Erythema Heatmap"):
            st.markdown("""
                *The CIE-Lab $a^*$ axis (green to red) separates chromatic vascular flushing from melanin pigmentation. 
                Below is the thermal radiance map of micro-erythema across the facial dermis:*
            """)
            st.image(cv2.cvtColor(cv_res.erythema.erythema_heatmap_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)

        # Detailed breakdown tables
        st.markdown("#### Quantitative Metric Breakdown")
        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(f"""
                <div class="luxury-card">
                    <h4 style="margin: 0 0 0.5rem 0; color: #22D3EE;">T-Zone vs U-Zone Sebum</h4>
                    <p style="font-size: 0.82rem; color: #94A3B8;">
                        • <strong>T-Zone (Forehead & Nose)</strong>: {cv_res.sebum.t_zone_sebum_score:.3f}<br>
                        • <strong>U-Zone (Cheeks & Chin)</strong>: {cv_res.sebum.u_zone_sebum_score:.3f}<br>
                        • <strong>Specular Ratio</strong>: {cv_res.sebum.specular_ratio * 100:.2f}% of pixels<br>
                        • <strong>Classification</strong>: {cv_res.sebum.sebum_classification}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with b2:
            st.markdown(f"""
                <div class="luxury-card">
                    <h4 style="margin: 0 0 0.5rem 0; color: #A78BFA;">CIE-Lab Colorimetry</h4>
                    <p style="font-size: 0.82rem; color: #94A3B8;">
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
                    <h4 style="margin: 0 0 0.5rem 0; color: #34D399;">Texture & Micro-Relief</h4>
                    <p style="font-size: 0.82rem; color: #94A3B8;">
                        • <strong>Laplacian Variance</strong>: {cv_res.texture.laplacian_variance:.1f}<br>
                        • <strong>Roughness Score</strong>: {cv_res.texture.roughness_score:.3f}<br>
                        • <strong>Active Blemishes</strong>: {cv_res.texture.active_blemish_count} spots<br>
                        • <strong>Lesion Density</strong>: {cv_res.texture.blemish_density_per_kpx:.2f} / kpx
                    </p>
                </div>
            """, unsafe_allow_html=True)


# =====================================================================
# TAB 2: FORMULATED COSMECEUTICAL REGIMEN
# =====================================================================
with tab2:
    if st.session_state.regimen_result is None:
        st.markdown("""
            <div class="luxury-card" style="text-align: center; padding: 2.5rem 1rem; margin-top: 1rem;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🧪</div>
                <div style="font-weight: 600; font-size: 1.1rem; color: #F8FAFC; margin-bottom: 0.4rem;">Regimen Synthesis Pending</div>
                <div style="font-size: 0.88rem; color: #94A3B8; max-width: 500px; margin: 0 auto;">
                    Run the skin diagnostic in the sidebar or from the home tab to formulate your individualized AM/PM cosmeceutical active protocol.
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        regimen: FormulatedRegimen = st.session_state.regimen_result
        cv_res: SkinAnalysisResult = st.session_state.analysis_result
        intake: ClinicalIntakeData = st.session_state.intake_data
        cross_val: IntakeCrossValidation = st.session_state.cross_val

        # Safety Clearance
        render_safety_banner(regimen.safety_clearance)

        # Profile Summary Card
        st.markdown(f"""
            <div class="luxury-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span class="pill-badge pill-violet">Engine: {regimen.engine_used}</span>
                    <span class="pill-badge pill-cyan">Reconciled: {cross_val.reconciled_skin_type}</span>
                </div>
                <h3 style="margin: 0.2rem 0; font-size: 1.15rem; color: #F8FAFC;">Clinical Dermatological Assessment</h3>
                <p style="color: #94A3B8; font-size: 0.88rem; line-height: 1.6; margin-bottom: 0.5rem;">
                    {regimen.skin_profile_summary}
                </p>
                <div style="font-size: 0.78rem; color: #64748B;">
                    Evaluation Horizon: {regimen.expected_timeline_weeks} weeks • Tolerance: {cross_val.tolerance_rating}
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


# =====================================================================
# TAB 3: CHEMICAL KNOWLEDGE GRAPH (28 ACTIVES)
# =====================================================================
with tab3:
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

    # Filter
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


# =====================================================================
# TAB 4: SYSTEM ARCHITECTURE & CLINICAL SCIENCE
# =====================================================================
with tab4:
    st.markdown("### 📐 Technical Architecture & Clinical Science")
    st.markdown("""
        SkinnAlgo is engineered to bridge **applied computer vision**, **deterministic safety constraint satisfaction**, and **multimodal generative synthesis**.
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


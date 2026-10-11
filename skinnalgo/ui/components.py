"""
Reusable Luxury UI Components for SkinnAlgo.
Renders metric meters, AM/PM routine timelines, safety banners, and compound cards.
"""

from typing import List
import streamlit as st

from skinnalgo.cv.pipeline import SkinAnalysisResult
from skinnalgo.recommender.fallback_engine import FormulatedRegimen, RoutineStep
from skinnalgo.chemistry.knowledge_graph import CosmeceuticalCompound
from skinnalgo.chemistry.safety_engine import SafetyEngineValidationResult


def render_header():
    """Renders the top branding header with luxury typography and badges."""
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.8rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.07);">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="width: 44px; height: 44px; border-radius: 13px; background: radial-gradient(circle at 35% 30%, rgba(99, 102, 241, 0.35) 0%, rgba(20, 22, 32, 0.95) 75%); border: 1px solid rgba(99, 102, 241, 0.45); display: flex; align-items: center; justify-content: center; font-size: 1.35rem; box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);">
                    🔬
                </div>
                <div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.45rem; font-weight: 700; letter-spacing: -0.03em; color: #F8FAFC;">SkinnAlgo</span>
                        <span style="font-size: 0.68rem; font-weight: 600; padding: 2px 7px; border-radius: 9999px; background: rgba(99, 102, 241, 0.15); color: #818CF8; border: 1px solid rgba(99, 102, 241, 0.3);">v1.2</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #64748B; margin-top: 2px;">
                        Multimodal Skin Condition Intelligence & Cosmeceutical Compound Recommender
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 8px;">
                <span class="pill-badge pill-emerald">Deterministic Clearance</span>
                <span class="pill-badge pill-cyan">CIE-Lab Colorimetry</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_empty_hero():
    """Renders the flagship empty state studio with luxury action cards."""
    st.markdown("""
        <div class="brand-hero-container">
            <div class="brand-avatar-wrapper">
                <span style="font-size: 2rem;">🔬</span>
            </div>
            <div class="brand-title">Where should we begin?</div>
            <div class="brand-subtitle">
                Upload a facial portrait or select a clinical preset profile in the sidebar to run anthropometric landmark zoning, specular lipid quantification, and formulated cosmeceutical synthesis.
            </div>
        </div>
        
        <div style="max-width: 820px; margin: 0 auto 2.5rem auto;">
            <div class="hero-action-card">
                <div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem; margin-bottom: 2px;">Sebum & Lipid Sheen Analysis</div>
                    <div style="font-size: 0.82rem; color: #94A3B8;">HSV specular reflectance isolates sebaceous gland activity across T-Zone and U-Zone landmarks.</div>
                </div>
                <span class="pill-badge pill-cyan">HSV Physics</span>
            </div>
            <div class="hero-action-card">
                <div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem; margin-bottom: 2px;">Vascular Erythema Colorimetry</div>
                    <div style="font-size: 0.82rem; color: #94A3B8;">CIE-Lab a* chrominance modeling decouples melanin pigmentation from micro-flush inflammation.</div>
                </div>
                <span class="pill-badge pill-emerald">CIE-Lab a*</span>
            </div>
            <div class="hero-action-card">
                <div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem; margin-bottom: 2px;">Surface Micro-Relief & Lesion Density</div>
                    <div style="font-size: 0.82rem; color: #94A3B8;">Discrete 2D Laplacian gradient variance quantifies texture roughness and active blemishes.</div>
                </div>
                <span class="pill-badge pill-violet">Laplacian σ²</span>
            </div>
            <div class="hero-action-card">
                <div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem; margin-bottom: 2px;">Deterministic Chemical Safety Clearance</div>
                    <div style="font-size: 0.82rem; color: #94A3B8;">Hard-coded constraint graph intercepts 28+ active compound collisions (Retinoid/Acid, Redox clashes, SPF lock).</div>
                </div>
                <span class="pill-badge pill-amber">Zero Collision</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_cards(cv_result: SkinAnalysisResult):
    """Renders 4 glassmorphic diagnostic metric cards."""
    c1, c2, c3, c4 = st.columns(4)

    # 1. Sebum Metric Card
    with c1:
        sebum_score = cv_result.sebum.overall_sebum_score
        pill_class = "pill-cyan" if sebum_score < 0.25 else "pill-amber"
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Sebum / Shine Index</div>
                <div class="metric-val">{sebum_score:.2f} <span style="font-size: 0.8rem; color: #64748B;">/ 1.0</span></div>
                <div class="metric-subtitle">
                    <span class="pill-badge {pill_class}">{cv_result.sebum.sebum_classification}</span>
                </div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.5rem;">
                    T-Zone: {cv_result.sebum.t_zone_sebum_score:.2f} | U-Zone: {cv_result.sebum.u_zone_sebum_score:.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 2. Erythema Metric Card
    with c2:
        erythema_idx = cv_result.erythema.erythema_index
        pill_class = "pill-emerald" if erythema_idx < 0.20 else ("pill-amber" if erythema_idx < 0.45 else "pill-rose")
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Erythema (Redness) Index</div>
                <div class="metric-val">{erythema_idx:.2f} <span style="font-size: 0.8rem; color: #64748B;">/ 1.0</span></div>
                <div class="metric-subtitle">
                    <span class="pill-badge {pill_class}">{cv_result.erythema.erythema_severity}</span>
                </div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.5rem;">
                    CIE-Lab a*: {cv_result.erythema.mean_a_star:.1f} | Area: {cv_result.erythema.erythema_percentage:.1f}%
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 3. Texture & Blemishes
    with c3:
        roughness = cv_result.texture.roughness_score
        blemishes = cv_result.texture.active_blemish_count
        pill_class = "pill-emerald" if blemishes <= 2 else ("pill-amber" if blemishes <= 6 else "pill-rose")
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Texture & Lesions</div>
                <div class="metric-val">{blemishes} <span style="font-size: 0.8rem; color: #64748B;">spots</span></div>
                <div class="metric-subtitle">
                    <span class="pill-badge {pill_class}">{cv_result.texture.texture_classification}</span>
                </div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.5rem;">
                    Laplacian Var: {cv_result.texture.laplacian_variance:.1f} | Roughness: {roughness:.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 4. Overall Health Index
    with c4:
        health_idx = cv_result.skin_health_index
        pill_class = "pill-emerald" if health_idx >= 75 else ("pill-amber" if health_idx >= 50 else "pill-rose")
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Skin Health Index</div>
                <div class="metric-val">{health_idx} <span style="font-size: 0.8rem; color: #64748B;">/ 100</span></div>
                <div class="metric-subtitle">
                    <span class="pill-badge {pill_class}">Composite Score</span>
                </div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.5rem;">
                    Primary: {cv_result.primary_cv_concern}
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_safety_banner(safety: SafetyEngineValidationResult):
    """Renders deterministic safety clearance status."""
    if safety.violations:
        st.markdown("""
            <div style="background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.3); border-radius: 12px; padding: 1.2rem; margin: 1.2rem 0;">
                <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.6rem;">
                    <span class="pill-badge pill-rose">Safety Engine Intercept</span>
                    <strong style="color: #FB7185; font-size: 0.95rem;">Chemical Contraindication Blocked</strong>
                </div>
        """, unsafe_allow_html=True)
        for v in safety.violations:
            st.markdown(f"""
                <div style="margin-left: 0.5rem; margin-bottom: 0.5rem; font-size: 0.85rem; color: #E2E8F0;">
                    <div><strong>{v.title}</strong>: {v.biochemical_rationale}</div>
                    <div style="color: #34D399; margin-top: 0.2rem;">↳ <em>Clinical Override: {v.clinical_resolution}</em></div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 10px; padding: 0.8rem 1.2rem; margin: 1rem 0; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <span class="pill-badge pill-emerald">Deterministic Clearance</span>
                    <span style="font-size: 0.85rem; color: #E2E8F0;">Regimen fully compliant with biochemical safety rules. Zero ingredient collisions detected.</span>
                </div>
                <span class="pill-badge pill-emerald">SPF 50+ Photoprotection Enforced</span>
            </div>
        """, unsafe_allow_html=True)


def render_routine_steps(steps: List[RoutineStep], session_prefix: str = "am"):
    """Renders step-by-step cosmeceutical routine cards."""
    for s in steps:
        st.markdown(f"""
            <div class="routine-step">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="step-num">Step {s.step_number} — {s.step_type}</span>
                    <span class="pill-badge pill-violet">{s.concentration}</span>
                </div>
                <div class="step-compound">{s.compound_name}</div>
                <div class="step-moa">{s.mechanism_of_action}</div>
                <div style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 0.6rem;">
                    <strong>Directions:</strong> {s.instructions}
                </div>
                <div class="search-box">
                    <span>Search Query: {s.search_query}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_compound_card(comp: CosmeceuticalCompound):
    """Renders chemical knowledge graph profile card."""
    photo_pill = '<span class="pill-badge pill-amber">Photosensitizing (SPF Required)</span>' if comp.photosensitizing else '<span class="pill-badge pill-emerald">Non-Photosensitizing</span>'
    concerns = " • ".join([c.replace('_', ' ').title() for c in comp.target_concerns])

    st.markdown(f"""
        <div class="luxury-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill-badge pill-cyan">{comp.chemical_class}</span>
                    <h3 style="margin: 0.3rem 0 0.1rem 0; font-size: 1.2rem; color: #F8FAFC;">{comp.name}</h3>
                    <div style="font-size: 0.76rem; color: #64748B; font-family: monospace;">INCI: {comp.inci_name}</div>
                </div>
                <div style="text-align: right;">
                    <span class="pill-badge pill-violet">Optimal Conc: {comp.typical_concentration}</span>
                    <div style="font-size: 0.74rem; color: #64748B; margin-top: 0.25rem;">pH {comp.optimal_ph} | {comp.recommended_timing}</div>
                </div>
            </div>
            <div style="margin-top: 0.8rem; font-size: 0.84rem; color: #94A3B8; line-height: 1.5;">
                <strong>Biochemical MOA:</strong> {comp.mechanism_of_action}
            </div>
            <div style="margin-top: 0.6rem; font-size: 0.78rem; color: #CBD5E1;">
                <strong>Target Concerns:</strong> {concerns}
            </div>
            <div style="margin-top: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                {photo_pill}
                <div class="search-box" style="flex: 1; margin-left: 1rem;">
                    <span>{comp.search_query_template}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


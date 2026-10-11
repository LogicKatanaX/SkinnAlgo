"""
Unit tests for the Multimodal Regimen Formulation and Export Engine.
"""

import numpy as np
import pytest

from skinnalgo.cv.pipeline import SkinAnalysisResult
from skinnalgo.cv.sebum import SebumMetricResult
from skinnalgo.cv.erythema import ErythemaMetricResult
from skinnalgo.cv.texture_blemish import TextureMetricResult
from skinnalgo.cv.face_mesh import FacialROIs
from skinnalgo.clinical.questionnaire import (
    ClinicalIntakeData,
    IntakeCrossValidation,
    ClinicalAssessmentEngine,
)
from skinnalgo.recommender.fallback_engine import (
    DeterministicRegimenSynthesizer,
    FormulatedRegimen,
)
from skinnalgo.recommender.gemini_engine import GeminiRegimenRecommender
from skinnalgo.recommender.export import RoutineExporter


@pytest.fixture
def mock_cv_result():
    dummy_mask = np.full((100, 100), 255, dtype=np.uint8)
    dummy_img = np.full((100, 100, 3), 150, dtype=np.uint8)
    return SkinAnalysisResult(
        sebum=SebumMetricResult(
            overall_sebum_score=0.45,
            t_zone_sebum_score=0.55,
            u_zone_sebum_score=0.35,
            specular_ratio=0.12,
            sebum_classification="Oily",
            specular_mask=dummy_mask
        ),
        erythema=ErythemaMetricResult(
            erythema_index=0.18,
            mean_a_star=135.5,
            erythema_percentage=12.0,
            erythema_severity="Mild Vascular Flush",
            erythema_heatmap_bgr=dummy_img
        ),
        texture=TextureMetricResult(
            roughness_score=0.60,
            laplacian_variance=120.0,
            active_blemish_count=7,
            blemish_density_per_kpx=0.7,
            detected_blemishes=[],
            texture_classification="Moderate Texture & Blemishes"
        ),
        rois=FacialROIs(
            face_box=(10, 10, 80, 80),
            t_zone_mask=dummy_mask,
            u_zone_mask=dummy_mask,
            skin_mask=dummy_mask,
            forehead_roi=(20, 10, 60, 20),
            nose_roi=(35, 30, 30, 30),
            left_cheek_roi=(10, 35, 25, 25),
            right_cheek_roi=(65, 35, 25, 25),
            chin_roi=(30, 65, 40, 20),
            t_zone_polygons=[],
            u_zone_polygons=[]
        ),
        skin_health_index=65,
        primary_cv_concern="Active Breakouts & Inflammation",
        diagnostic_overlay_bgr=dummy_img,
        annotated_overlay_bgr=dummy_img,
        raw_image_bgr=dummy_img
    )


@pytest.fixture
def mock_intake():
    return ClinicalIntakeData(
        post_wash_feel="shiny_all_over",
        environment="dry_arid",
        barrier_reactivity="resilient",
        primary_goal="clear_breakouts"
    )


def test_cross_validation_logic(mock_intake):
    engine = ClinicalAssessmentEngine()
    cv = engine.cross_validate(
        intake=mock_intake,
        cv_sebum_score=0.45,
        cv_erythema_index=0.18,
        cv_blemish_count=7
    )
    assert isinstance(cv, IntakeCrossValidation)
    assert "Oily" in cv.reconciled_skin_type
    assert cv.tolerance_rating == "High / Resilient"


def test_deterministic_regimen_synthesis(mock_cv_result, mock_intake):
    engine = ClinicalAssessmentEngine()
    cross_val = engine.cross_validate(mock_intake, 0.45, 0.18, 7)

    synthesizer = DeterministicRegimenSynthesizer()
    regimen = synthesizer.synthesize(mock_cv_result, mock_intake, cross_val)

    assert isinstance(regimen, FormulatedRegimen)
    assert len(regimen.am_routine) >= 3
    assert len(regimen.pm_routine) >= 3

    # AM must include SPF photoprotection as final step
    am_last = regimen.am_routine[-1]
    assert "Photoprotection" in am_last.step_type or "SPF" in am_last.compound_name

    # PM must include Cleanser, Corrective Active, Barrier Cream
    step_types = [s.step_type for s in regimen.pm_routine]
    assert any("Cleanser" in st for st in step_types)
    assert any("Barrier" in st for st in step_types)


def test_routine_markdown_export(mock_cv_result, mock_intake):
    engine = ClinicalAssessmentEngine()
    cross_val = engine.cross_validate(mock_intake, 0.45, 0.18, 7)
    synthesizer = DeterministicRegimenSynthesizer()
    regimen = synthesizer.synthesize(mock_cv_result, mock_intake, cross_val)

    md = RoutineExporter.to_markdown(regimen, mock_cv_result, mock_intake, cross_val)
    assert "# 🔬 SkinnAlgo Clinical Cosmeceutical Regimen" in md
    assert "Morning (AM) Regimen" in md
    assert "SPF 50+" in md


def test_gemini_recommender_fallback_without_key(mock_cv_result, mock_intake):
    """Gemini recommender without API key must gracefully use fallback engine with zero error."""
    recommender = GeminiRegimenRecommender(api_key=None)
    engine = ClinicalAssessmentEngine()
    cross_val = engine.cross_validate(mock_intake, 0.45, 0.18, 7)

    regimen = recommender.formulate(mock_cv_result, mock_intake, cross_val)
    assert isinstance(regimen, FormulatedRegimen)
    assert len(regimen.am_routine) >= 3
    assert len(regimen.pm_routine) >= 3


def test_gemini_prompt_builder(mock_cv_result, mock_intake):
    recommender = GeminiRegimenRecommender(api_key="mock_key")
    engine = ClinicalAssessmentEngine()
    cross_val = engine.cross_validate(mock_intake, 0.45, 0.18, 7)

    prompt = recommender.build_prompt_payload(mock_cv_result, mock_intake, cross_val)
    assert "0.450" in prompt
    assert "CIE-Lab Mean a*" in prompt
    assert "HARD CHEMICAL SAFETY RULES" in prompt

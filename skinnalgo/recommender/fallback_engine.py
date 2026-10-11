"""
Deterministic Clinical Fallback Regimen Synthesizer.
Formulates structured, evidence-based cosmeceutical regimens completely offline
based on validated dermatological decision trees.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from skinnalgo.cv.pipeline import SkinAnalysisResult
from skinnalgo.clinical.questionnaire import ClinicalIntakeData, IntakeCrossValidation
from skinnalgo.chemistry.knowledge_graph import COMPOUND_DATABASE, CosmeceuticalCompound
from skinnalgo.chemistry.safety_engine import ChemicalSafetyEngine, SafetyEngineValidationResult


@dataclass
class RoutineStep:
    """A concrete application step in an AM or PM skincare routine."""
    step_number: int
    step_type: str                   # "Cleanser", "Treatment Active", "Moisturizer / Barrier", "Photoprotection"
    compound_name: str
    concentration: str
    mechanism_of_action: str
    instructions: str
    search_query: str


@dataclass
class FormulatedRegimen:
    """Complete multimodal cosmeceutical regimen recommendation."""
    skin_profile_summary: str
    am_routine: List[RoutineStep]
    pm_routine: List[RoutineStep]
    safety_clearance: SafetyEngineValidationResult
    clinical_precautions: List[str]
    expected_timeline_weeks: int
    engine_used: str                 # "Deterministic Clinical Rule Engine" or "Google Gemini Multimodal Fusion"


class DeterministicRegimenSynthesizer:
    """
    Expert system implementing evidence-based clinical decision algorithms.
    Guarantees 100% test reproducibility and offline operational resilience.
    """

    def __init__(self):
        self.safety_engine = ChemicalSafetyEngine()

    def synthesize(
        self,
        cv_result: SkinAnalysisResult,
        intake: ClinicalIntakeData,
        cross_val: IntakeCrossValidation
    ) -> FormulatedRegimen:
        """
        Formulate an optimized AM/PM regimen fusing CV colorimetry and intake profile.
        """
        am_candidates: List[str] = []
        pm_candidates: List[str] = []
        precautions: List[str] = []

        sebum_score = cv_result.sebum.overall_sebum_score
        erythema_idx = cv_result.erythema.erythema_index
        blemishes = cv_result.texture.active_blemish_count
        goal = intake.primary_goal
        barrier_low = cross_val.barrier_compromised_risk

        # -------------------------------------------------------------
        # Decision Logic by Primary Objective and Clinical Metrics
        # -------------------------------------------------------------
        if barrier_low or erythema_idx > 0.40:
            # Protocol: Barrier Recovery & Neurovascular Calming
            am_candidates = ["niacinamide", "ceramides_np_ap_eop"]
            pm_candidates = ["centella_asiatica", "panthenol", "ceramides_np_ap_eop"]
            precautions.append("Acute Barrier Recovery Phase: Active chemical exfoliants paused for 14 days.")
            precautions.append("Focus solely on lipid replenishment, transepidermal hydration, and UV defense.")
            profile_sum = "Compromised Moisture Barrier with Reactive Erythema. Intensive lipid bilayer repair prioritized."
            timeline = 3

        elif goal == "clear_breakouts" or blemishes >= 5:
            # Protocol: Comedolytic & Antimicrobial
            if cross_val.tolerance_rating == "Fragile / Low":
                am_candidates = ["azelaic_acid", "ceramides_np_ap_eop"]
                pm_candidates = ["gluconolactone", "panthenol", "ceramides_np_ap_eop"]
                precautions.append("Sensitive acne profile: Using Azelaic Acid + Polyhydroxy Acid (PHA) to avoid barrier trauma.")
            else:
                am_candidates = ["niacinamide", "zinc_pca", "ceramides_np_ap_eop"]
                pm_candidates = ["adapalene", "ceramides_np_ap_eop"]
                precautions.append("Retinoid Purging Note: Mild flaking or micro-breakouts may occur between weeks 2-4 as follicular microcomedones are cleared.")
                precautions.append("Use the sandwich method (Moisturizer -> Adapalene -> Moisturizer) if mild tightness occurs.")
            profile_sum = f"Acne-Prone Epidermis with {blemishes} detected surface lesions. Follicular desquamation and microbial suppression indicated."
            timeline = 8

        elif goal == "fade_dark_spots":
            # Protocol: Multi-Pathway Tyrosinase & Melanin Transfer Inhibition
            am_candidates = ["ethyl_ascorbic_acid", "ceramides_np_ap_eop"]
            pm_candidates = ["tranexamic_acid", "alpha_arbutin", "ceramides_np_ap_eop"]
            precautions.append("Hyperpigmentation Protocol: Direct sunlight triggers melanogenesis within 15 minutes. Broad-spectrum SPF reapplication every 2 hours outdoors is mandatory.")
            profile_sum = "Post-Inflammatory Hyperpigmentation (PIH) / Dyschromia. Multi-target melanogenesis suppression indicated."
            timeline = 12

        elif goal == "control_oil_pores" or sebum_score > 0.35:
            # Protocol: Seboregulation & Pore Architecture Refinement
            am_candidates = ["niacinamide", "zinc_pca", "ceramides_np_ap_eop"]
            pm_candidates = ["salicylic_acid", "ceramides_np_ap_eop"]
            precautions.append("Sebum Regulation: Do not skip nighttime barrier moisturizer; stripping lipids triggers compensatory sebum rebound.")
            profile_sum = f"Hyperseborrheic Skin (CV Sebum Score: {sebum_score:.2f}). Follicular lipophilic desmolysis and 5-alpha reductase inhibition indicated."
            timeline = 6

        elif goal == "smooth_texture" or cv_result.texture.roughness_score > 0.45:
            # Protocol: Epidermal Renewal & Desquamation
            am_candidates = ["niacinamide", "ceramides_np_ap_eop"]
            pm_candidates = ["glycolic_acid", "ceramides_np_ap_eop"]
            precautions.append("Chemical Exfoliation Protocol: Limit Glycolic Acid application to 2-3 nights per week initially.")
            profile_sum = f"Surface Texture Roughness (Laplacian score {cv_result.texture.roughness_score:.2f}). Desmosome lysis and basal renewal indicated."
            timeline = 6

        else:
            # Protocol: Eudermic Maintenance & Pro-Collagen Longevity
            am_candidates = ["ethyl_ascorbic_acid", "ceramides_np_ap_eop"]
            pm_candidates = ["bakuchiol", "hyaluronic_acid_multi", "ceramides_np_ap_eop"]
            profile_sum = "Balanced Eudermic Profile. Antioxidant photoprotection and collagen preservation indicated."
            timeline = 8

        # Enforce Deterministic Safety Engine
        safety_result = self.safety_engine.validate_regimen(
            am_compound_ids=am_candidates,
            pm_compound_ids=pm_candidates,
            barrier_compromised=barrier_low,
            erythema_index=erythema_idx
        )

        # Assemble Morning Routine Steps
        am_steps: List[RoutineStep] = []
        step_idx = 1

        # Step 1: Cleanser
        if sebum_score > 0.30:
            am_steps.append(RoutineStep(
                step_number=step_idx,
                step_type="Purifying Cleanser",
                compound_name="Gentle Gel Cleanser with Zinc & Glycerin",
                concentration="pH 5.5 Balanced",
                mechanism_of_action="Surfactant micellar system that removes nighttime sebum secretions without disrupting the stratum corneum acid mantle.",
                instructions="Lather with lukewarm water for 30 seconds. Rinse thoroughly and pat dry with a clean microfiber towel.",
                search_query="Gentle foaming facial gel cleanser pH 5.5 sulfate-free fragrance-free"
            ))
        else:
            am_steps.append(RoutineStep(
                step_number=step_idx,
                step_type="Hydrating Cleanser",
                compound_name="Gentle Cream-to-Foam Amino Acid Cleanser",
                concentration="Physiological pH 5.0",
                mechanism_of_action="Sodium cocoyl glycinate lipid cleanser that preserves intercellular lipids and Natural Moisturizing Factors (NMF).",
                instructions="Massage gently onto damp face. Rinse without rubbing.",
                search_query="Gentle hydrating cream cleanser ceramide fragrance-free non-foaming"
            ))
        step_idx += 1

        # Step 2: Morning Active(s)
        for cid in safety_result.sanitized_am_compounds:
            comp = COMPOUND_DATABASE.get(cid)
            if comp and comp.chemical_class != "Stratum Corneum Barrier Lipid":
                am_steps.append(RoutineStep(
                    step_number=step_idx,
                    step_type="Target Active Treatment",
                    compound_name=comp.name,
                    concentration=comp.typical_concentration,
                    mechanism_of_action=comp.mechanism_of_action,
                    instructions="Dispense 3-4 drops across fingertips. Lightly press into cleansed face and neck until absorbed.",
                    search_query=comp.search_query_template
                ))
                step_idx += 1

        # Step 3: Barrier Moisturizer
        am_steps.append(RoutineStep(
            step_number=step_idx,
            step_type="Barrier Moisturizer",
            compound_name="Physiological Ceramide (NP, AP, EOP) Emulsion",
            concentration="3:1:1 Physiological Lipid Ratio",
            mechanism_of_action="Restores intercellular lipid lamellae, prevents Transepidermal Water Loss (TEWL), and calms subclinical erythema.",
            instructions="Smooth an almond-sized amount evenly over face.",
            search_query="Physiological Ceramide 3:1:1 light daily moisturizer lotion fragrance-free"
        ))
        step_idx += 1

        # Step 4: Broad-Spectrum SPF 50+
        am_steps.append(RoutineStep(
            step_number=step_idx,
            step_type="Photoprotection (Mandatory)",
            compound_name="Broad-Spectrum UV Filters SPF 50+ PA++++",
            concentration="SPF 50+ / Critical Wavelength >370nm",
            mechanism_of_action="Organic/inorganic UV filter matrix that absorbs and scatters UVA/UVB photons, preventing photon-induced melanocyte activation, collagen matrix metalloproteinase breakdown, and reactive oxygen species generation.",
            instructions="Apply generous two-finger length (1/4 tsp) to face, ears, and neck 15 minutes before daylight exposure. Reapply every 2 hours if outdoors.",
            search_query="Broad Spectrum Sunscreen SPF 50 PA++++ invisible finish non-comedogenic fragrance-free"
        ))

        # Assemble Evening Routine Steps
        pm_steps: List[RoutineStep] = []
        step_idx = 1

        # Step 1: Cleanser
        pm_steps.append(RoutineStep(
            step_number=step_idx,
            step_type="Deep / Double Cleanser",
            compound_name="Barrier-Gentle Micellar Gel or Oil Cleanser",
            concentration="Surfactant Emollient Matrix",
            mechanism_of_action="Solubilizes lipophilic sunscreen polymers, airborne particulates, and oxidized surface sebum without stripping cellular ceramides.",
            instructions="Massage onto dry skin for 45 seconds to break down sunscreen and oil, emulsify with water, then rinse clean.",
            search_query="Gentle cleansing oil or micellar gel wash fragrance-free non-comedogenic"
        ))
        step_idx += 1

        # Step 2: Night Active Treatment(s)
        for cid in safety_result.sanitized_pm_compounds:
            comp = COMPOUND_DATABASE.get(cid)
            if comp and comp.chemical_class != "Stratum Corneum Barrier Lipid" and cid != "panthenol":
                pm_steps.append(RoutineStep(
                    step_number=step_idx,
                    step_type="Primary Corrective Active",
                    compound_name=comp.name,
                    concentration=comp.typical_concentration,
                    mechanism_of_action=comp.mechanism_of_action,
                    instructions="Apply a pea-sized amount evenly to completely dry skin. Avoid direct contact with ocular orbital rim and mucosal lips.",
                    search_query=comp.search_query_template
                ))
                step_idx += 1

        # Step 3: Nighttime Barrier Restoration Cream
        pm_steps.append(RoutineStep(
            step_number=step_idx,
            step_type="Lipid Barrier Cream",
            compound_name="Bio-Identical Ceramide & Panthenol Barrier Cream",
            concentration="5% Panthenol + Multi-Ceramide Complex",
            mechanism_of_action="Delivers biomimetic lipids and pro-vitamin B5 overnight to catalyze keratinocyte renewal, support stratum corneum envelope integrity, and accelerate tissue recuperation.",
            instructions="Gently press into face and neck as the final sealing step.",
            search_query="5% Panthenol B5 Ceramide Barrier Recovery Cream fragrance-free"
        ))

        return FormulatedRegimen(
            skin_profile_summary=profile_sum,
            am_routine=am_steps,
            pm_routine=pm_steps,
            safety_clearance=safety_result,
            clinical_precautions=precautions,
            expected_timeline_weeks=timeline,
            engine_used="Deterministic Clinical Rule Engine"
        )


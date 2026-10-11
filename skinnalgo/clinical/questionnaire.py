"""
Interactive Clinical Intake Assessment & Cross-Validation Engine.
Reconciles patient self-reported sensory indications with objective CV metrics.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class ClinicalIntakeData:
    """Standardized responses from the 4-question clinical intake."""
    post_wash_feel: str          # "tight_parched", "balanced_supple", "shiny_all_over", "oily_t_zone_only"
    environment: str             # "dry_arid", "humid_tropical", "high_pollution", "cold_windy"
    barrier_reactivity: str      # "stings_easily", "fragrance_reactive", "resilient"
    primary_goal: str            # "clear_breakouts", "fade_dark_spots", "repair_barrier", "control_oil_pores", "smooth_texture"


@dataclass
class IntakeCrossValidation:
    """Clinical reconciliation between questionnaire and computer vision metrics."""
    reconciled_skin_type: str
    barrier_compromised_risk: bool
    clinical_flags: List[str]
    photoprotection_priority: str
    tolerance_rating: str         # "Fragile / Low", "Moderate", "High / Resilient"


class ClinicalAssessmentEngine:
    """
    Evaluates clinical intake and performs cross-modality diagnostic reconciliation.
    """

    POST_WASH_LABELS = {
        "tight_parched": "Tight, parched, and uncomfortable (Dry)",
        "balanced_supple": "Comfortable, hydrated, neither dry nor oily (Balanced)",
        "shiny_all_over": "Greasy or shiny all over forehead & cheeks (Oily)",
        "oily_t_zone_only": "Shiny on forehead & nose, normal or dry cheeks (Combination)",
    }

    ENVIRONMENT_LABELS = {
        "dry_arid": "Dry / Arid / Heavy indoor climate control (Low humidity)",
        "humid_tropical": "Humid / Tropical (High moisture & sweat)",
        "high_pollution": "Dense urban environment / Heavy airborne particulate",
        "cold_windy": "Cold / Harsh winter winds (Barrier stress)",
    }

    BARRIER_LABELS = {
        "stings_easily": "Easily reactive / Stings or burns with common moisturizers (High sensitivity)",
        "fragrance_reactive": "Flushes or reacts to essential oils / fragrances (Moderate sensitivity)",
        "resilient": "Tolerant / Rarely irritates or reddens (High resilience)",
    }

    GOAL_LABELS = {
        "clear_breakouts": "Clear active breakouts & inflammatory papules",
        "fade_dark_spots": "Fade post-inflammatory dark spots & hyperpigmentation",
        "repair_barrier": "Repair compromised skin barrier & soothe redness",
        "control_oil_pores": "Regulate sebum oiliness & refine pore texture",
        "smooth_texture": "Smooth surface roughness & boost cellular renewal",
    }

    def cross_validate(
        self,
        intake: ClinicalIntakeData,
        cv_sebum_score: float,
        cv_erythema_index: float,
        cv_blemish_count: int
    ) -> IntakeCrossValidation:
        """
        Reconciles subjective intake with objective colorimetry & CV indicators.
        """
        flags: List[str] = []
        barrier_compromised = False

        # Tolerance rating
        if intake.barrier_reactivity == "stings_easily" or cv_erythema_index > 0.45:
            tolerance = "Fragile / Low"
            barrier_compromised = True
            flags.append("High Barrier Reactivity Detected: Direct high-percentage chemical acids contra-indicated.")
        elif intake.barrier_reactivity == "fragrance_reactive" or cv_erythema_index > 0.28:
            tolerance = "Moderate"
        else:
            tolerance = "High / Resilient"

        # Reconcile skin type: Dehydrated-Oily breakdown
        if intake.post_wash_feel == "tight_parched" and cv_sebum_score > 0.25:
            reconciled_type = "Dehydrated Oily (Lipid overproduction secondary to Transepidermal Water Loss)"
            barrier_compromised = True
            flags.append("Clinical Mismatch: Sensory tightness with elevated surface shine indicates impaired moisture barrier.")
        elif intake.post_wash_feel == "shiny_all_over" or cv_sebum_score > 0.40:
            reconciled_type = "Hyperseborrheic / Oily"
        elif intake.post_wash_feel == "oily_t_zone_only" or (cv_sebum_score > 0.22):
            reconciled_type = "Combination (Sebaceous T-Zone / Normal U-Zone)"
        elif intake.post_wash_feel == "tight_parched" or cv_sebum_score < 0.10:
            reconciled_type = "Alipic / Dry (Lipid Deficient)"
        else:
            reconciled_type = "Eudermic / Balanced"

        # Active breakout vs PIH priority
        if intake.primary_goal == "fade_dark_spots" and cv_blemish_count >= 5:
            flags.append("Triage Note: Active inflammatory breakouts detected alongside hyperpigmentation. Calming acute breakouts prioritized before aggressive tyrosinase inhibitors.")

        # Environmental factors
        if intake.environment in ("dry_arid", "cold_windy"):
            flags.append(f"Environmental Factor: {intake.environment.replace('_', ' ').title()} demands biomimetic occlusives and ceramide fortification.")
        elif intake.environment == "high_pollution":
            flags.append("Environmental Factor: High oxidative urban exposure calls for daytime topical antioxidants (Ectoin / Stabilized Vitamin C derivative).")

        # Photoprotection
        photoprotection = "Mandatory Broad-Spectrum SPF 50+ PA++++ (High UV defense essential for active regimen)"

        return IntakeCrossValidation(
            reconciled_skin_type=reconciled_type,
            barrier_compromised_risk=barrier_compromised,
            clinical_flags=flags,
            photoprotection_priority=photoprotection,
            tolerance_rating=tolerance
        )


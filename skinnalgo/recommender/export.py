"""
Routine Exporter: Markdown and Clinical Summary Generation.
Produces clean, printable cosmeceutical routine documentation.
"""

from skinnalgo.cv.pipeline import SkinAnalysisResult
from skinnalgo.clinical.questionnaire import ClinicalIntakeData, IntakeCrossValidation
from skinnalgo.recommender.fallback_engine import FormulatedRegimen


class RoutineExporter:
    """Exports structured regimen results into clinical Markdown reports."""

    @staticmethod
    def to_markdown(
        regimen: FormulatedRegimen,
        cv_result: SkinAnalysisResult,
        intake: ClinicalIntakeData,
        cross_val: IntakeCrossValidation
    ) -> str:
        lines = []
        lines.append("# 🔬 SkinnAlgo Clinical Cosmeceutical Regimen")
        lines.append(f"**Engine**: {regimen.engine_used} | **Health Index**: {cv_result.skin_health_index}/100")
        lines.append(f"**Reconciled Skin Type**: {cross_val.reconciled_skin_type}")
        lines.append(f"**Target Objective**: {intake.primary_goal.replace('_', ' ').title()}")
        lines.append(f"**Tolerance Level**: {cross_val.tolerance_rating}")
        lines.append("")

        lines.append("## 📊 Diagnostic Metrics Summary")
        lines.append(f"- **Sebum Score**: {cv_result.sebum.overall_sebum_score:.3f} ({cv_result.sebum.sebum_classification})")
        lines.append(f"  * T-Zone: {cv_result.sebum.t_zone_sebum_score:.3f} | U-Zone: {cv_result.sebum.u_zone_sebum_score:.3f}")
        lines.append(f"- **Erythema Index**: {cv_result.erythema.erythema_index:.3f} (Lab a*: {cv_result.erythema.mean_a_star:.1f}) — {cv_result.erythema.erythema_severity}")
        lines.append(f"- **Texture Roughness**: {cv_result.texture.roughness_score:.3f} ({cv_result.texture.texture_classification})")
        lines.append(f"- **Active Lesions**: {cv_result.texture.active_blemish_count} detected")
        lines.append("")

        lines.append("## 📋 Clinical Profile Summary")
        lines.append(regimen.skin_profile_summary)
        lines.append("")

        lines.append("---")
        lines.append("## ☀️ Morning (AM) Regimen")
        for step in regimen.am_routine:
            lines.append(f"### Step {step.step_number}: {step.step_type}")
            lines.append(f"**Active Compound**: {step.compound_name} ({step.concentration})")
            lines.append(f"- **Mechanism of Action**: {step.mechanism_of_action}")
            lines.append(f"- **Application**: {step.instructions}")
            lines.append(f"- **Search Query**: `{step.search_query}`")
            lines.append("")

        lines.append("---")
        lines.append("## 🌙 Evening (PM) Regimen")
        for step in regimen.pm_routine:
            lines.append(f"### Step {step.step_number}: {step.step_type}")
            lines.append(f"**Active Compound**: {step.compound_name} ({step.concentration})")
            lines.append(f"- **Mechanism of Action**: {step.mechanism_of_action}")
            lines.append(f"- **Application**: {step.instructions}")
            lines.append(f"- **Search Query**: `{step.search_query}`")
            lines.append("")

        lines.append("---")
        lines.append("## 🛡️ Safety Engine Clearances & Precautions")
        lines.append(f"- **Mandatory SPF 50+ Photoprotection**: {'Enforced' if regimen.safety_clearance.mandatory_spf_enforced else 'Standard'}")
        lines.append(f"- **Barrier Recovery Mode**: {'ACTIVE (Actives paused)' if regimen.safety_clearance.barrier_recovery_mode else 'Normal Maintenance'}")

        if regimen.safety_clearance.violations:
            lines.append("\n### Intercepted Chemical Contraindications:")
            for v in regimen.safety_clearance.violations:
                lines.append(f"- ⚠️ **{v.title}**: {v.biochemical_rationale}")
                lines.append(f"  * *Resolution*: {v.clinical_resolution}")

        if regimen.clinical_precautions:
            lines.append("\n### Clinical Notes:")
            for p in regimen.clinical_precautions:
                lines.append(f"- {p}")

        lines.append(f"\n*Expected clinical evaluation window: {regimen.expected_timeline_weeks} weeks.*")
        lines.append("\n*Disclaimer: SkinnAlgo is an educational cosmetic formulation assistant and does not provide medical diagnoses.*")

        return "\n".join(lines)


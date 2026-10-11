"""
Google Gemini Multimodal Formulation & Regimen Generator.
Fuses CV quantitative colorimetry, clinical intake responses, and deterministic safety rules
into evidence-based personalized cosmeceutical routines.
"""

import json
import os
from typing import Dict, List, Optional
from google import genai
from google.genai import types

from skinnalgo.cv.pipeline import SkinAnalysisResult
from skinnalgo.clinical.questionnaire import ClinicalIntakeData, IntakeCrossValidation
from skinnalgo.chemistry.knowledge_graph import COMPOUND_DATABASE, CosmeceuticalCompound
from skinnalgo.chemistry.safety_engine import ChemicalSafetyEngine, SafetyEngineValidationResult
from skinnalgo.recommender.fallback_engine import (
    DeterministicRegimenSynthesizer,
    FormulatedRegimen,
    RoutineStep,
)


class GeminiRegimenRecommender:
    """
    Multimodal formulation recommender powered by Google Gemini.
    Features robust error recovery with seamless fallback to deterministic clinical algorithms.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None
        self.fallback_engine = DeterministicRegimenSynthesizer()
        self.safety_engine = ChemicalSafetyEngine()

    def build_prompt_payload(
        self,
        cv_result: SkinAnalysisResult,
        intake: ClinicalIntakeData,
        cross_val: IntakeCrossValidation
    ) -> str:
        """
        Builds structured clinical context prompt for Gemini.
        """
        prompt = f"""
You are the AI Cosmeceutical Decision Engine for SkinnAlgo. Formulate an evidence-based, clinical-grade active skincare chemical regimen. 
You do NOT diagnose medical pathology. You recommend exact chemical compound names, physiological concentrations, biochemical Mechanisms of Action (MOA), and product search queries.

### 1. PATIENT QUANTITATIVE COMPUTER VISION METRICS
- Sebum Overall Score: {cv_result.sebum.overall_sebum_score:.3f} / 1.000 ({cv_result.sebum.sebum_classification})
  * T-Zone Sebum: {cv_result.sebum.t_zone_sebum_score:.3f}
  * U-Zone Sebum: {cv_result.sebum.u_zone_sebum_score:.3f}
  * Specular Highlight Ratio: {cv_result.sebum.specular_ratio:.4f}
- Erythema (Redness) Colorimetric Index: {cv_result.erythema.erythema_index:.3f} / 1.000
  * CIE-Lab Mean a* Channel: {cv_result.erythema.mean_a_star:.2f} (Neutral is 128.0)
  * Facial Micro-Erythema Coverage: {cv_result.erythema.erythema_percentage:.1f}%
  * Severity Rating: {cv_result.erythema.erythema_severity}
- Texture & Surface Roughness:
  * Roughness Score: {cv_result.texture.roughness_score:.3f} / 1.000
  * Laplacian Gradient Variance: {cv_result.texture.laplacian_variance:.1f}
  * Active Detected Surface Lesions: {cv_result.texture.active_blemish_count}
  * Texture Classification: {cv_result.texture.texture_classification}
- Composite Skin Health Index: {cv_result.skin_health_index} / 100
- Primary CV Surface Concern: {cv_result.primary_cv_concern}

### 2. CLINICAL INTAKE & CROSS-VALIDATION
- Sensory Skin Feel (2h post-wash): {intake.post_wash_feel}
- Environmental Exposure: {intake.environment}
- Barrier Reactivity / Sensitivity: {intake.barrier_reactivity}
- Primary Therapeutic Objective: {intake.primary_goal}
- Reconciled Skin Type: {cross_val.reconciled_skin_type}
- Barrier Compromised Risk: {cross_val.barrier_compromised_risk}
- Tolerance Rating: {cross_val.tolerance_rating}
- Clinical Triage Flags: {", ".join(cross_val.clinical_flags) if cross_val.clinical_flags else "None"}

### 3. HARD CHEMICAL SAFETY RULES (DETERMINISTIC CONSTRAINTS)
1. NEVER pair Retinoids (Adapalene/Retinol) with strong chemical exfoliants (AHA/BHA) in the same PM routine.
2. NEVER mix Benzoyl Peroxide with pure L-Ascorbic Acid simultaneously (redox oxidation conflict).
3. If Barrier Compromised Risk is TRUE or Erythema Index > 0.40, suspend direct keratolytics and mandate Ceramide 3:1:1 + Panthenol barrier recovery.
4. Mandatory Broad-Spectrum SPF 50+ PA++++ is strictly non-negotiable for AM Step 4.

### 4. REQUIRED OUTPUT FORMAT
Return a STRICT JSON object with the following schema:
{{
  "skin_profile_summary": "Concise 2-sentence clinical dermatological assessment.",
  "expected_timeline_weeks": 6,
  "clinical_precautions": ["precaution 1", "precaution 2"],
  "am_routine": [
    {{
      "step_number": 1,
      "step_type": "Cleanser",
      "compound_name": "...",
      "concentration": "...",
      "mechanism_of_action": "...",
      "instructions": "...",
      "search_query": "..."
    }}
  ],
  "pm_routine": [
    {{
      "step_number": 1,
      "step_type": "Cleanser",
      "compound_name": "...",
      "concentration": "...",
      "mechanism_of_action": "...",
      "instructions": "...",
      "search_query": "..."
    }}
  ]
}}
"""
        return prompt.strip()

    def formulate(
        self,
        cv_result: SkinAnalysisResult,
        intake: ClinicalIntakeData,
        cross_val: IntakeCrossValidation
    ) -> FormulatedRegimen:
        """
        Synthesize regimen via Google Gemini, falling back to deterministic synthesizer
        if API key is unavailable or request fails.
        """
        # If no client or API key, run deterministic fallback
        if not self.client:
            return self.fallback_engine.synthesize(cv_result, intake, cross_val)

        try:
            prompt = self.build_prompt_payload(cv_result, intake, cross_val)
            
            # Using Gemini 2.5 Flash for ultra-fast, high-accuracy structured reasoning
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                )
            )

            data = json.loads(response.text)

            # Parse routine steps
            am_steps = [
                RoutineStep(
                    step_number=s.get("step_number", idx + 1),
                    step_type=s.get("step_type", "Step"),
                    compound_name=s.get("compound_name", ""),
                    concentration=s.get("concentration", ""),
                    mechanism_of_action=s.get("mechanism_of_action", ""),
                    instructions=s.get("instructions", ""),
                    search_query=s.get("search_query", "")
                )
                for idx, s in enumerate(data.get("am_routine", []))
            ]

            pm_steps = [
                RoutineStep(
                    step_number=s.get("step_number", idx + 1),
                    step_type=s.get("step_type", "Step"),
                    compound_name=s.get("compound_name", ""),
                    concentration=s.get("concentration", ""),
                    mechanism_of_action=s.get("mechanism_of_action", ""),
                    instructions=s.get("instructions", ""),
                    search_query=s.get("search_query", "")
                )
                for idx, s in enumerate(data.get("pm_routine", []))
            ]

            # Re-verify through deterministic safety engine to guarantee zero hallucinated hazards
            am_c_ids = [s.compound_name.lower().replace(" ", "_") for s in am_steps]
            pm_c_ids = [s.compound_name.lower().replace(" ", "_") for s in pm_steps]
            safety_res = self.safety_engine.validate_regimen(
                am_compound_ids=am_c_ids,
                pm_compound_ids=pm_c_ids,
                barrier_compromised=cross_val.barrier_compromised_risk,
                erythema_index=cv_result.erythema.erythema_index
            )

            return FormulatedRegimen(
                skin_profile_summary=data.get("skin_profile_summary", "Multimodal dermatological profile synthesized."),
                am_routine=am_steps,
                pm_routine=pm_steps,
                safety_clearance=safety_res,
                clinical_precautions=data.get("clinical_precautions", []),
                expected_timeline_weeks=int(data.get("expected_timeline_weeks", 6)),
                engine_used="Google Gemini Multimodal Fusion"
            )

        except Exception as e:
            # Fallback gracefully
            fallback = self.fallback_engine.synthesize(cv_result, intake, cross_val)
            fallback.clinical_precautions.append(f"(Gemini API note: Switched to deterministic clinical engine: {str(e)[:60]})")
            return fallback


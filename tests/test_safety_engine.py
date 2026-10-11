"""
Unit tests for the Deterministic Chemical Safety and Contraindication Rule Engine.
"""

import pytest
from skinnalgo.chemistry.safety_engine import ChemicalSafetyEngine, SafetyEngineValidationResult


@pytest.fixture
def engine():
    return ChemicalSafetyEngine()


def test_rule_1_retinoid_acid_collision(engine):
    """Pairing Adapalene with Salicylic Acid in PM must trigger critical contraindication."""
    res = engine.validate_regimen(
        am_compound_ids=["niacinamide"],
        pm_compound_ids=["adapalene", "salicylic_acid"]
    )
    assert not res.is_safe
    assert len(res.violations) >= 1
    assert any("RETINOID-ACID-COLLISION" in v.rule_id for v in res.violations)
    # The acid must be sanitized out of PM
    assert "salicylic_acid" not in res.sanitized_pm_compounds
    assert "adapalene" in res.sanitized_pm_compounds


def test_rule_1_retinol_glycolic_collision(engine):
    """Pairing Retinol with Glycolic Acid in PM must trigger collision."""
    res = engine.validate_regimen(
        am_compound_ids=["niacinamide"],
        pm_compound_ids=["retinol", "glycolic_acid"]
    )
    assert not res.is_safe
    assert any("RETINOID-ACID-COLLISION" in v.rule_id for v in res.violations)


def test_rule_2_bpo_vitc_redox_conflict(engine):
    """Simultaneous AM co-application of BPO and pure L-Ascorbic Acid must trigger redox intercept."""
    res = engine.validate_regimen(
        am_compound_ids=["benzoyl_peroxide", "l_ascorbic_acid"],
        pm_compound_ids=["ceramides_np_ap_eop"]
    )
    assert not res.is_safe
    assert any("BPO-VITC-REDOX-CONFLICT" in v.rule_id for v in res.violations)
    # Must substitute pure L-Ascorbic Acid with stabilized non-acidic derivative
    assert "l_ascorbic_acid" not in res.sanitized_am_compounds
    assert "ethyl_ascorbic_acid" in res.sanitized_am_compounds


def test_rule_3_copper_peptide_acid_warning(engine):
    """Pairing Copper Tripeptide-1 with direct acid in PM must trigger warning."""
    res = engine.validate_regimen(
        am_compound_ids=["niacinamide"],
        pm_compound_ids=["copper_tripeptide_1", "lactic_acid"]
    )
    assert any("COPPER-PEPTIDE" in w.rule_id for w in res.warnings)
    assert "copper_tripeptide_1" not in res.sanitized_pm_compounds


def test_rule_4_compromised_barrier_override(engine):
    """When barrier is compromised, harsh keratolytics must be suspended and Ceramides injected."""
    res = engine.validate_regimen(
        am_compound_ids=["salicylic_acid"],
        pm_compound_ids=["glycolic_acid"],
        barrier_compromised=True,
        erythema_index=0.55
    )
    assert res.barrier_recovery_mode is True
    # Strong acids removed
    assert "salicylic_acid" not in res.sanitized_am_compounds
    assert "glycolic_acid" not in res.sanitized_pm_compounds
    # Restorative lipids injected
    assert "ceramides_np_ap_eop" in res.sanitized_am_compounds
    assert "ceramides_np_ap_eop" in res.sanitized_pm_compounds
    assert "panthenol" in res.sanitized_pm_compounds


def test_rule_5_mandatory_spf_enforcement(engine):
    """Recommending photosensitizers (Adapalene/Glycolic Acid) must enforce mandatory SPF 50+."""
    res = engine.validate_regimen(
        am_compound_ids=["niacinamide"],
        pm_compound_ids=["adapalene"]
    )
    assert res.mandatory_spf_enforced is True


def test_safe_compatible_regimen_passes(engine):
    """Compatible synergistic pairing (Niacinamide AM + Adapalene PM) must pass cleanly."""
    res = engine.validate_regimen(
        am_compound_ids=["niacinamide", "zinc_pca"],
        pm_compound_ids=["adapalene", "ceramides_np_ap_eop"]
    )
    assert res.is_safe is True
    assert len(res.violations) == 0


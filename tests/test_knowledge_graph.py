"""
Unit tests for the Cosmeceutical Knowledge Graph and Compound Database.
"""

import pytest
from skinnalgo.chemistry.knowledge_graph import (
    COMPOUND_DATABASE,
    CosmeceuticalCompound,
    CosmeceuticalKnowledgeGraph,
)


@pytest.fixture
def kg():
    return CosmeceuticalKnowledgeGraph()


def test_database_count(kg):
    """Knowledge graph must contain at least 25 clinically verified active compounds."""
    compounds = kg.all_compounds()
    assert len(compounds) >= 25
    assert len(compounds) == 28


def test_compound_field_completeness(kg):
    """Every compound in the database must possess full clinical and chemical metadata."""
    for cid, c in kg.compounds.items():
        assert isinstance(c, CosmeceuticalCompound)
        assert c.id == cid
        assert len(c.name.strip()) > 0
        assert len(c.inci_name.strip()) > 0
        assert len(c.chemical_class.strip()) > 0
        assert len(c.typical_concentration.strip()) > 0
        assert len(c.optimal_ph.strip()) > 0
        assert len(c.target_concerns) > 0
        assert len(c.mechanism_of_action.strip()) > 20
        assert isinstance(c.photosensitizing, bool)
        assert c.recommended_timing in ("AM", "PM", "AM/PM", "PM_ONLY")
        assert len(c.search_query_template.strip()) > 0


def test_search_by_concern_acne(kg):
    """Searching for 'acne' concern must retrieve key anti-acne actives."""
    results = kg.search_by_concern("acne")
    result_ids = [c.id for c in results]
    assert "salicylic_acid" in result_ids
    assert "adapalene" in result_ids
    assert "benzoyl_peroxide" in result_ids


def test_search_by_concern_barrier(kg):
    """Searching for 'barrier' concern must retrieve lipid and soothing actives."""
    results = kg.search_by_concern("barrier")
    result_ids = [c.id for c in results]
    assert "ceramides_np_ap_eop" in result_ids
    assert "panthenol" in result_ids
    assert "centella_asiatica" in result_ids


def test_search_by_concern_erythema(kg):
    """Searching for 'erythema' concern must retrieve anti-redness actives."""
    results = kg.search_by_concern("erythema")
    result_ids = [c.id for c in results]
    assert "azelaic_acid" in result_ids
    assert "centella_asiatica" in result_ids


def test_photosensitizers_flagged(kg):
    """Photosensitizing actives must have photosensitizing set to True."""
    adapalene = kg.get("adapalene")
    glycolic = kg.get("glycolic_acid")
    niacinamide = kg.get("niacinamide")

    assert adapalene.photosensitizing is True
    assert glycolic.photosensitizing is True
    assert niacinamide.photosensitizing is False


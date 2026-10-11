"""
Unit tests for CIE-Lab colorimetry and Erythema Index calculations.
"""

import numpy as np
import pytest
from skinnalgo.cv.erythema import ErythemaAnalyzer, ErythemaMetricResult


@pytest.fixture
def analyzer():
    return ErythemaAnalyzer()


def test_neutral_gray_erythema(analyzer):
    """A neutral gray image should have low erythema index."""
    gray_img = np.full((100, 100, 3), 128, dtype=np.uint8)
    mask = np.full((100, 100), 255, dtype=np.uint8)

    res = analyzer.compute_erythema_index(gray_img, mask)
    assert isinstance(res, ErythemaMetricResult)
    assert 0.0 <= res.erythema_index <= 0.15
    assert "Minimal" in res.erythema_severity


def test_high_erythema_red_patch(analyzer):
    """An inflamed red patch should produce high erythema index and marked severity."""
    red_img = np.zeros((100, 100, 3), dtype=np.uint8)
    red_img[:, :] = (50, 60, 220)  # High BGR Red
    mask = np.full((100, 100), 255, dtype=np.uint8)

    res = analyzer.compute_erythema_index(red_img, mask)
    assert res.erythema_index > 0.40
    assert res.mean_a_star > 140.0
    assert res.erythema_percentage > 50.0


def test_erythema_bounds(analyzer):
    """Erythema index must always remain strictly bounded in [0.0, 1.0]."""
    for color in [(0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255)]:
        img = np.full((50, 50, 3), color, dtype=np.uint8)
        mask = np.full((50, 50), 255, dtype=np.uint8)
        res = analyzer.compute_erythema_index(img, mask)
        assert 0.0 <= res.erythema_index <= 1.0


def test_empty_mask_handling(analyzer):
    """Empty mask should fallback safely without throwing division by zero."""
    img = np.full((50, 50, 3), 150, dtype=np.uint8)
    mask = np.zeros((50, 50), dtype=np.uint8)

    res = analyzer.compute_erythema_index(img, mask)
    assert isinstance(res, ErythemaMetricResult)
    assert 0.0 <= res.erythema_index <= 1.0


def test_fitzpatrick_tone_melanin_resilience(analyzer):
    """Melanin darkening (lower L) should not falsely inflate a* erythema."""
    # Synthetic darker skin patch without redness: BGR (70, 90, 120)
    dark_skin = np.full((100, 100, 3), (70, 90, 120), dtype=np.uint8)
    mask = np.full((100, 100), 255, dtype=np.uint8)

    res = analyzer.compute_erythema_index(dark_skin, mask)
    # Without vascular redness, delta a* should remain low
    assert res.erythema_index < 0.35


def test_heatmap_dimension_integrity(analyzer):
    """Generated thermal heatmap must match input image dimensions."""
    img = np.full((120, 80, 3), 140, dtype=np.uint8)
    mask = np.full((120, 80), 255, dtype=np.uint8)

    res = analyzer.compute_erythema_index(img, mask)
    assert res.erythema_heatmap_bgr.shape == (120, 80, 3)


"""
Unit tests for Sebum & Specular Reflection algorithms.
"""

import numpy as np
import pytest
from skinnalgo.cv.sebum import SebumAnalyzer, SebumMetricResult


@pytest.fixture
def analyzer():
    return SebumAnalyzer()


def test_matte_skin_zero_specular(analyzer):
    """Matte skin patch (diffuse reflection) should yield low sebum score."""
    matte_img = np.full((100, 100, 3), (130, 160, 200), dtype=np.uint8)  # BGR
    t_mask = np.full((100, 100), 255, dtype=np.uint8)
    u_mask = np.full((100, 100), 255, dtype=np.uint8)

    res = analyzer.analyze(matte_img, t_mask, u_mask)
    assert isinstance(res, SebumMetricResult)
    assert res.overall_sebum_score < 0.25
    assert res.specular_ratio < 0.05


def test_oily_specular_hotspot(analyzer):
    """Bright specular highlight (high V, low S) should produce high sebum score."""
    shiny_img = np.full((100, 100, 3), (140, 170, 210), dtype=np.uint8)
    # Inject specular highlight patch
    shiny_img[20:60, 20:60] = (255, 255, 255)

    t_mask = np.full((100, 100), 255, dtype=np.uint8)
    u_mask = np.full((100, 100), 255, dtype=np.uint8)

    res = analyzer.analyze(shiny_img, t_mask, u_mask)
    assert res.overall_sebum_score > 0.30
    assert res.specular_ratio > 0.05


def test_combination_skin_differentiation(analyzer):
    """High T-Zone shine with low U-Zone shine should classify as Combination or Dehydrated-Oily."""
    img = np.full((100, 100, 3), (120, 150, 190), dtype=np.uint8)
    # T-Zone top half has shine
    img[:50, :] = (250, 250, 250)

    t_mask = np.zeros((100, 100), dtype=np.uint8)
    t_mask[:50, :] = 255
    u_mask = np.zeros((100, 100), dtype=np.uint8)
    u_mask[50:, :] = 255

    res = analyzer.analyze(img, t_mask, u_mask)
    assert res.t_zone_sebum_score > res.u_zone_sebum_score
    assert res.sebum_classification in ("Combination", "Dehydrated-Oily")


def test_sebum_score_bounds(analyzer):
    """Sebum scores must strictly lie in [0.0, 1.0]."""
    for val in [0, 50, 128, 200, 255]:
        img = np.full((60, 60, 3), val, dtype=np.uint8)
        mask = np.full((60, 60), 255, dtype=np.uint8)
        res = analyzer.analyze(img, mask, mask)
        assert 0.0 <= res.overall_sebum_score <= 1.0
        assert 0.0 <= res.t_zone_sebum_score <= 1.0
        assert 0.0 <= res.u_zone_sebum_score <= 1.0


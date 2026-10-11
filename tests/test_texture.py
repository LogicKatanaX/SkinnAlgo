"""
Unit tests for Skin Texture Roughness and Blemish Detection.
"""

import cv2
import numpy as np
import pytest
from skinnalgo.cv.texture_blemish import TextureBlemishAnalyzer, TextureMetricResult


@pytest.fixture
def analyzer():
    return TextureBlemishAnalyzer()


def test_glass_skin_zero_roughness(analyzer):
    """Uniformly smooth patch should have near zero Laplacian variance."""
    smooth_gray = np.full((120, 120), 160, dtype=np.uint8)
    mask = np.full((120, 120), 255, dtype=np.uint8)

    roughness, variance = analyzer.compute_texture_roughness(smooth_gray, mask)
    assert roughness < 0.05
    assert variance < 1.0


def test_textured_skin_high_variance(analyzer):
    """Patch with high spatial noise should produce high Laplacian variance."""
    np.random.seed(42)
    noise_gray = np.random.randint(50, 200, (120, 120), dtype=np.uint8)
    mask = np.full((120, 120), 255, dtype=np.uint8)

    roughness, variance = analyzer.compute_texture_roughness(noise_gray, mask)
    assert roughness > 0.50
    assert variance > 100.0


def test_blemish_isolation(analyzer):
    """Synthetic circular inflammatory spot should be detected as blemish."""
    img = np.full((150, 150, 3), (160, 190, 220), dtype=np.uint8)
    # Draw circular red papule
    cv2.circle(img, (75, 75), 8, (60, 60, 240), -1)
    mask = np.full((150, 150), 255, dtype=np.uint8)

    blemishes = analyzer.detect_blemishes(img, mask)
    assert len(blemishes) >= 1
    detected = blemishes[0]
    # Check center is near (75, 75)
    assert abs(detected.center[0] - 75) <= 5
    assert abs(detected.center[1] - 75) <= 5
    assert detected.category == "papule/inflammatory"


def test_texture_analysis_result_structure(analyzer):
    """Full analyze method must return properly structured and bounded results."""
    img = np.full((100, 100, 3), 150, dtype=np.uint8)
    mask = np.full((100, 100), 255, dtype=np.uint8)

    res = analyzer.analyze(img, mask)
    assert isinstance(res, TextureMetricResult)
    assert 0.0 <= res.roughness_score <= 1.0
    assert res.active_blemish_count >= 0
    assert isinstance(res.texture_classification, str)


"""
Unit tests for Facial Landmark and ROI Segmentation.
"""

import numpy as np
import pytest
from skinnalgo.cv.face_mesh import FaceROISegmenter, FacialROIs


@pytest.fixture
def segmenter():
    return FaceROISegmenter()


def test_face_detection_fallback(segmenter):
    """Uniform dummy image should safely fallback to center crop without crashing."""
    img = np.full((400, 300, 3), 100, dtype=np.uint8)
    fx, fy, fw, fh = segmenter.detect_face(img)
    assert 0 <= fx < 300
    assert 0 <= fy < 400
    assert fw > 0 and fh > 0


def test_roi_segmentation_masks(segmenter):
    """segment_rois must return non-empty T-Zone and U-Zone masks."""
    img = np.full((600, 500, 3), (160, 190, 220), dtype=np.uint8)
    rois = segmenter.segment_rois(img)

    assert isinstance(rois, FacialROIs)
    assert rois.t_zone_mask.shape == (600, 500)
    assert rois.u_zone_mask.shape == (600, 500)
    assert np.count_nonzero(rois.t_zone_mask) > 0
    assert np.count_nonzero(rois.u_zone_mask) > 0


def test_roi_subcomponents(segmenter):
    """Forehead, nose, cheeks, and chin ROIs must be within valid image boundaries."""
    img = np.full((700, 600, 3), (160, 190, 220), dtype=np.uint8)
    rois = segmenter.segment_rois(img)

    for roi in [rois.forehead_roi, rois.nose_roi, rois.left_cheek_roi, rois.right_cheek_roi, rois.chin_roi]:
        x, y, w, h = roi
        assert x >= 0 and y >= 0
        assert w > 0 and h > 0
        assert x + w <= 600
        assert y + h <= 700


def test_skin_mask_locus(segmenter):
    """Skin locus filter should extract skin-toned pixels and suppress blue/green non-skin pixels."""
    skin_img = np.full((100, 100, 3), (160, 195, 230), dtype=np.uint8)  # Natural skin BGR
    blue_img = np.full((100, 100, 3), (255, 0, 0), dtype=np.uint8)      # Pure Blue BGR

    skin_mask = segmenter.extract_skin_mask(skin_img)
    blue_mask = segmenter.extract_skin_mask(blue_img)

    assert np.count_nonzero(skin_mask) > 8000
    assert np.count_nonzero(blue_mask) == 0


"""
Blemish Detection and Skin Texture Roughness Density Analysis.
Computes Laplacian gradient variance and morphological lesion clusters.
"""

from dataclasses import dataclass
from typing import List, Tuple
import cv2
import numpy as np


@dataclass
class BlemishDetection:
    """Represents a localized detected blemish or texture irregularity."""
    center: Tuple[int, int]
    radius: int
    category: str        # "papule/inflammatory", "comedone/texture", "hyperpigmentation"
    confidence: float


@dataclass
class TextureMetricResult:
    """Quantitative results from texture and blemish profiling."""
    roughness_score: float                # 0.0 (Glassy/Smooth) to 1.0 (Rough/Textured)
    laplacian_variance: float             # Raw micro-contrast gradient variance
    active_blemish_count: int             # Count of detected surface lesions
    blemish_density_per_kpx: float        # Lesions per 1,000 skin pixels
    detected_blemishes: List[BlemishDetection]
    texture_classification: str           # Glass Skin, Refined, Moderate Texture, Pronounced Roughness


class TextureBlemishAnalyzer:
    """
    Evaluates micro-relief skin texture and isolates active blemish clusters.
    """

    def __init__(self, variance_norm_max: float = 350.0):
        self.variance_norm_max = variance_norm_max

    def compute_texture_roughness(
        self,
        gray_img: np.ndarray,
        roi_mask: np.ndarray
    ) -> Tuple[float, float]:
        """
        Compute high-frequency spatial variation using 2D Laplacian operator.
        """
        laplacian = cv2.Laplacian(gray_img, cv2.CV_64F, ksize=3)
        valid_indices = roi_mask > 0

        if np.count_nonzero(valid_indices) == 0:
            return 0.0, 0.0

        lap_vals = laplacian[valid_indices]
        variance = float(np.var(lap_vals))

        # Normalized roughness score 0.0 to 1.0
        roughness = float(np.clip(variance / self.variance_norm_max, 0.0, 1.0))
        return roughness, variance

    def detect_blemishes(
        self,
        bgr_img: np.ndarray,
        roi_mask: np.ndarray
    ) -> List[BlemishDetection]:
        """
        Isolate localized inflammatory spots and hyperpigmented macules
        using adaptive thresholding and morphological blob analysis.
        """
        lab = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2Lab)
        l_channel = lab[:, :, 0]
        a_channel = lab[:, :, 1]

        # Contrast-enhanced redness for inflammatory lesions
        a_diff = cv2.absdiff(a_channel, cv2.GaussianBlur(a_channel, (15, 15), 0))
        # Contrast-enhanced darkness for hyperpigmentation / closed comedones
        l_diff = cv2.absdiff(l_channel, cv2.GaussianBlur(l_channel, (15, 15), 0))

        # Threshold top deviations within skin mask
        _, thresh_red = cv2.threshold(a_diff, 10, 255, cv2.THRESH_BINARY)
        _, thresh_dark = cv2.threshold(l_diff, 14, 255, cv2.THRESH_BINARY)

        thresh_combined = cv2.bitwise_or(thresh_red, thresh_dark)
        thresh_combined = cv2.bitwise_and(thresh_combined, roi_mask)

        # Morphological opening to isolate circular spots
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opened = cv2.morphologyEx(thresh_combined, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections: List[BlemishDetection] = []
        h, w = bgr_img.shape[:2]
        min_area = max(4, int((h * w) * 0.00002))
        max_area = max(400, int((h * w) * 0.005))

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if min_area <= area <= max_area:
                perimeter = cv2.arcLength(cnt, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * (area / (perimeter * perimeter))
                    if circularity > 0.35:  # Reasonably circular lesion
                        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
                        cx, cy, r = int(cx), int(cy), max(4, int(radius))

                        # Classify type based on local color
                        sub_a = float(a_channel[max(0, cy - r):min(h, cy + r), max(0, cx - r):min(w, cx + r)].mean())
                        sub_l = float(l_channel[max(0, cy - r):min(h, cy + r), max(0, cx - r):min(w, cx + r)].mean())

                        if sub_a > 142:
                            cat = "papule/inflammatory"
                        elif sub_l < 110:
                            cat = "hyperpigmentation"
                        else:
                            cat = "comedone/texture"

                        confidence = min(0.95, round(0.50 + circularity * 0.45, 2))
                        detections.append(BlemishDetection(
                            center=(cx, cy),
                            radius=r,
                            category=cat,
                            confidence=confidence
                        ))

        # Limit to top 25 prominent blemishes to avoid visual clutter
        detections.sort(key=lambda d: d.confidence, reverse=True)
        return detections[:25]

    def analyze(
        self,
        bgr_img: np.ndarray,
        roi_mask: np.ndarray
    ) -> TextureMetricResult:
        """
        Analyze texture roughness and blemish distribution.
        """
        gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
        roughness, variance = self.compute_texture_roughness(gray, roi_mask)
        blemishes = self.detect_blemishes(bgr_img, roi_mask)

        skin_px_count = np.count_nonzero(roi_mask)
        blemish_density = float((len(blemishes) / max(1, skin_px_count)) * 1000.0)

        # Classification
        if roughness < 0.20 and len(blemishes) <= 2:
            classification = "Glass Skin / Ultra Smooth"
        elif roughness < 0.40 and len(blemishes) <= 5:
            classification = "Refined / Minimal Texture"
        elif roughness < 0.65 or len(blemishes) <= 12:
            classification = "Moderate Texture & Blemishes"
        else:
            classification = "Pronounced Roughness & Active Breakouts"

        return TextureMetricResult(
            roughness_score=round(roughness, 3),
            laplacian_variance=round(variance, 1),
            active_blemish_count=len(blemishes),
            blemish_density_per_kpx=round(blemish_density, 3),
            detected_blemishes=blemishes,
            texture_classification=classification
        )

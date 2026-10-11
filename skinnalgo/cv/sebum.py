"""
Quantitative Sebum & Specular Reflection Metric.
Quantifies skin lipid shine across T-Zone and U-Zone regions of interest.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import cv2
import numpy as np


@dataclass
class SebumMetricResult:
    """Quantitative results from sebum & shine analysis."""
    overall_sebum_score: float         # 0.0 (Matte/Dry) to 1.0 (Hyperseborrheic)
    t_zone_sebum_score: float          # 0.0 to 1.0
    u_zone_sebum_score: float          # 0.0 to 1.0
    specular_ratio: float              # Proportion of highlight pixels
    sebum_classification: str          # Dry, Balanced, Combination, Oily, Dehydrated-Oily
    specular_mask: np.ndarray          # Binary mask of detected specular highlights


class SebumAnalyzer:
    """
    Computes specular reflection and luminance peaks to quantify facial sebum production.
    Distinguishes between diffuse matte reflection and lipid specular highlights.
    """

    def __init__(self, value_thresh: int = 205, sat_max_thresh: int = 60):
        self.value_thresh = value_thresh
        self.sat_max_thresh = sat_max_thresh

    def detect_specular_highlights(self, bgr_img: np.ndarray, skin_mask: np.ndarray) -> np.ndarray:
        """
        Identify specular reflection hotspots (high value/luminance, low color saturation).
        """
        hsv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        v_channel = hsv[:, :, 2]
        s_channel = hsv[:, :, 1]

        # Specular reflection is bright (high V) and desaturated (low S)
        specular = (v_channel >= self.value_thresh) & (s_channel <= self.sat_max_thresh)
        specular_mask = (specular.astype(np.uint8) * 255)

        # Restrict to dermis area
        if skin_mask is not None and np.count_nonzero(skin_mask) > 0:
            specular_mask = cv2.bitwise_and(specular_mask, skin_mask)

        # Morphological filter to remove isolated sensor noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        specular_mask = cv2.morphologyEx(specular_mask, cv2.MORPH_OPEN, kernel)
        return specular_mask

    def calculate_zone_shine(
        self,
        specular_mask: np.ndarray,
        zone_mask: np.ndarray,
        gray_img: np.ndarray
    ) -> float:
        """
        Calculates shine score for a specific zone normalized between 0.0 and 1.0.
        Combines area ratio and luminance intensity peaks.
        """
        zone_pixels = np.count_nonzero(zone_mask)
        if zone_pixels == 0:
            return 0.0

        # Pixels with specular reflection in this zone
        specular_in_zone = cv2.bitwise_and(specular_mask, zone_mask)
        specular_count = np.count_nonzero(specular_in_zone)

        # Area ratio: usually ranges from 0% to ~25% in very shiny skin
        area_ratio = specular_count / zone_pixels
        # Normalize area ratio so 20% specular coverage maps to ~0.85
        normalized_ratio = min(1.0, area_ratio / 0.22)

        # Average luminance within the zone
        zone_gray_values = gray_img[zone_mask > 0]
        mean_lum = float(np.mean(zone_gray_values)) if len(zone_gray_values) > 0 else 128.0
        lum_factor = max(0.0, min(1.0, (mean_lum - 100.0) / 130.0))

        # Weighted combination: 70% specular highlight area + 30% baseline luminance
        score = (0.70 * normalized_ratio) + (0.30 * lum_factor)
        return float(np.clip(score, 0.0, 1.0))

    def analyze(
        self,
        bgr_img: np.ndarray,
        t_zone_mask: np.ndarray,
        u_zone_mask: np.ndarray,
        skin_mask: Optional[np.ndarray] = None
    ) -> SebumMetricResult:
        """
        Analyze sebum levels across T-Zone and U-Zone.
        """
        gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
        specular_mask = self.detect_specular_highlights(bgr_img, skin_mask)

        t_score = self.calculate_zone_shine(specular_mask, t_zone_mask, gray)
        u_score = self.calculate_zone_shine(specular_mask, u_zone_mask, gray)

        # Overall facial sebum: T-Zone is physiologically richer in sebaceous glands (60% weight)
        overall_score = float(np.clip((0.60 * t_score) + (0.40 * u_score), 0.0, 1.0))

        # Clinical skin type classification
        if t_score > 0.40 and u_score < 0.22:
            classification = "Combination"
        elif t_score > 0.35 and u_score > 0.28:
            classification = "Oily"
        elif t_score < 0.12 and u_score < 0.10:
            classification = "Dry"
        elif t_score > 0.30 and u_score < 0.15:
            classification = "Dehydrated-Oily"
        else:
            classification = "Balanced / Normal"

        total_skin = np.count_nonzero(t_zone_mask) + np.count_nonzero(u_zone_mask)
        total_spec = np.count_nonzero(cv2.bitwise_and(specular_mask, cv2.bitwise_or(t_zone_mask, u_zone_mask)))
        spec_ratio = float(total_spec / max(1, total_skin))

        return SebumMetricResult(
            overall_sebum_score=round(overall_score, 3),
            t_zone_sebum_score=round(t_score, 3),
            u_zone_sebum_score=round(u_score, 3),
            specular_ratio=round(spec_ratio, 4),
            sebum_classification=classification,
            specular_mask=specular_mask
        )

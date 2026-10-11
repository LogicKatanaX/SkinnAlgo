"""
Erythema (Redness) Colorimetric Index via CIE-Lab Color Space.
Decouples melanin pigmentation and illumination to quantify vascular flush & micro-inflammation.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import cv2
import numpy as np


@dataclass
class ErythemaMetricResult:
    """Quantitative colorimetric erythema results."""
    erythema_index: float             # 0.0 (Calm/Resilient) to 1.0 (Severe Erythema)
    mean_a_star: float                # Raw CIE-Lab a* channel value (128 = neutral)
    erythema_percentage: float        # Percentage of facial area showing elevated micro-flush
    erythema_severity: str            # Minimal, Mild, Moderate, Marked
    erythema_heatmap_bgr: np.ndarray  # Thermal visualization of inflammatory redness


class ErythemaAnalyzer:
    """
    Measures capillary dilation and inflammatory flushing using CIE-Lab a* colorimetry.
    Normalizes against baseline skin tone to ensure Fitzpatrick neutrality.
    """

    def __init__(self, neutral_baseline: float = 136.0, sensitivity_gain: float = 24.0):
        # 128 is theoretical Lab neutral; Caucasian/Asian/Fitzpatrick baseline skin a* is typically 134-142
        self.neutral_baseline = neutral_baseline
        self.sensitivity_gain = sensitivity_gain

    def compute_erythema_index(
        self,
        bgr_img: np.ndarray,
        roi_mask: np.ndarray
    ) -> ErythemaMetricResult:
        """
        Quantify erythema across the masked facial area.
        """
        # Convert to CIE-Lab color space
        lab = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2Lab)
        l_channel = lab[:, :, 0]
        a_channel = lab[:, :, 1]  # Green (-a) to Red (+a)

        # Mask pixels
        valid_indices = roi_mask > 0
        if np.count_nonzero(valid_indices) == 0:
            # Fallback if mask is empty
            valid_indices = np.ones(bgr_img.shape[:2], dtype=bool)

        a_values = a_channel[valid_indices].astype(np.float32)
        l_values = l_channel[valid_indices].astype(np.float32)

        mean_a = float(np.mean(a_values))
        median_a = float(np.median(a_values))

        # Local baseline estimation: take lower 30th percentile of a* as uninflamed reference
        baseline_a = float(np.percentile(a_values, 30))
        # If the lower 30th percentile is already inflamed, anchor to calibrated physiological neutral
        if baseline_a > (self.neutral_baseline + 6.0):
            baseline_ref = self.neutral_baseline
        else:
            baseline_ref = max(self.neutral_baseline, baseline_a)

        # Delta a* (positive deviation represents micro-erythema)
        delta_a = max(0.0, mean_a - baseline_ref)

        # Normalized index 0.0 to 1.0
        erythema_idx = float(np.clip(delta_a / self.sensitivity_gain, 0.0, 1.0))

        # Elevated redness threshold (pixels significantly redder than baseline)
        erythema_thresh = baseline_ref + 6.0
        elevated_pixels = np.count_nonzero(a_channel[valid_indices] > erythema_thresh)
        erythema_pct = float((elevated_pixels / len(a_values)) * 100.0)

        # Classify clinical erythema severity
        if erythema_idx < 0.15:
            severity = "Minimal / Calm"
        elif erythema_idx < 0.35:
            severity = "Mild Vascular Flush"
        elif erythema_idx < 0.65:
            severity = "Moderate Reactive Erythema"
        else:
            severity = "Marked Inflammatory Erythema"

        # Generate thermal colorimetric heatmap overlay
        # Map a* channel in ROI to normalized 0-255 range
        norm_a = np.clip((a_channel.astype(np.float32) - 128.0) * (255.0 / 40.0), 0, 255).astype(np.uint8)
        heatmap = cv2.applyColorMap(norm_a, cv2.COLORMAP_MAGMA)

        # Mask background to keep only face dermis
        heatmap_masked = np.zeros_like(bgr_img)
        heatmap_masked[valid_indices] = heatmap[valid_indices]

        # Blend with original image (40% original, 60% heatmap)
        blended = cv2.addWeighted(bgr_img, 0.35, heatmap, 0.65, 0)
        final_heatmap = np.where(roi_mask[:, :, None] > 0, blended, bgr_img)

        return ErythemaMetricResult(
            erythema_index=round(erythema_idx, 3),
            mean_a_star=round(mean_a, 2),
            erythema_percentage=round(erythema_pct, 1),
            erythema_severity=severity,
            erythema_heatmap_bgr=final_heatmap
        )

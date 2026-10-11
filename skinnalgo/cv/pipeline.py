"""
Unified Computer Vision Pipeline & Diagnostic Overlay Renderer.
Orchestrates landmark segmentation, colorimetry, sebum metrics, and texture profiling.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np

from skinnalgo.cv.face_mesh import FaceROISegmenter, FacialROIs
from skinnalgo.cv.sebum import SebumAnalyzer, SebumMetricResult
from skinnalgo.cv.erythema import ErythemaAnalyzer, ErythemaMetricResult
from skinnalgo.cv.texture_blemish import TextureBlemishAnalyzer, TextureMetricResult


@dataclass
class SkinAnalysisResult:
    """Comprehensive diagnostic results from the computer vision pipeline."""
    sebum: SebumMetricResult
    erythema: ErythemaMetricResult
    texture: TextureMetricResult
    rois: FacialROIs
    skin_health_index: int                # 0 to 100 holistic index
    primary_cv_concern: str               # "Active Breakouts", "Vascular Erythema", "Hyperseborrhea", "Texture", "Balanced"
    diagnostic_overlay_bgr: np.ndarray    # Clean visual overlay with ROIs and blemish rings
    annotated_overlay_bgr: np.ndarray     # Full annotated diagnostic canvas
    raw_image_bgr: np.ndarray


class SkinCVPipeline:
    """
    End-to-end computer vision and colorimetry pipeline.
    Combines deterministic multi-spectral color space analysis (HSV, CIE-Lab, YCrCb)
    with anthropometric facial landmark zoning.
    """

    def __init__(self):
        self.roi_segmenter = FaceROISegmenter()
        self.sebum_analyzer = SebumAnalyzer()
        self.erythema_analyzer = ErythemaAnalyzer()
        self.texture_analyzer = TextureBlemishAnalyzer()

    def render_overlay(
        self,
        bgr_img: np.ndarray,
        rois: FacialROIs,
        sebum_res: SebumMetricResult,
        erythema_res: ErythemaMetricResult,
        texture_res: TextureMetricResult
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Renders luxury diagnostic overlays adhering to Apple/iOS clean aesthetic:
        - T-Zone in subtle electric cyan
        - U-Zone in subtle amethyst violet
        - Blemishes in precision target reticles
        - Specular shine highlights in soft pearl glow
        """
        overlay = bgr_img.copy()
        clean_view = bgr_img.copy()

        # Draw semi-transparent T-Zone mask (Cyan: (212, 182, 6) in BGR)
        t_mask_color = np.zeros_like(bgr_img)
        cv2.fillPoly(t_mask_color, rois.t_zone_polygons, (212, 182, 6))
        # Draw semi-transparent U-Zone mask (Violet: (246, 92, 139) in BGR)
        u_mask_color = np.zeros_like(bgr_img)
        cv2.fillPoly(u_mask_color, rois.u_zone_polygons, (246, 92, 139))

        # Blend subtle zone tints
        cv2.addWeighted(overlay, 0.88, t_mask_color, 0.12, 0, overlay)
        cv2.addWeighted(overlay, 0.88, u_mask_color, 0.12, 0, overlay)

        # Draw fine zone borders
        for poly in rois.t_zone_polygons:
            cv2.polylines(overlay, [poly], isClosed=True, color=(240, 200, 30), thickness=2, lineType=cv2.LINE_AA)
            cv2.polylines(clean_view, [poly], isClosed=True, color=(240, 200, 30), thickness=2, lineType=cv2.LINE_AA)

        for poly in rois.u_zone_polygons:
            cv2.polylines(overlay, [poly], isClosed=True, color=(230, 110, 180), thickness=2, lineType=cv2.LINE_AA)
            cv2.polylines(clean_view, [poly], isClosed=True, color=(230, 110, 180), thickness=2, lineType=cv2.LINE_AA)

        # Draw subtle specular highlight indicators in soft amber
        spec_pts = np.argwhere(sebum_res.specular_mask > 0)
        if len(spec_pts) > 0:
            # Draw subsampled shine markers
            step = max(1, len(spec_pts) // 150)
            for pt in spec_pts[::step]:
                y, x = pt
                cv2.circle(overlay, (x, y), 1, (255, 235, 150), -1)

        # Draw blemish markers
        for b in texture_res.detected_blemishes:
            cx, cy = b.center
            r = max(5, b.radius)
            if b.category == "papule/inflammatory":
                color = (94, 63, 244)   # Rose Red in BGR
            elif b.category == "hyperpigmentation":
                color = (241, 102, 99)  # Deep Indigo in BGR
            else:
                color = (30, 160, 245)   # Amber in BGR

            # Sleek ring overlay
            cv2.circle(overlay, (cx, cy), r + 2, color, 1, cv2.LINE_AA)
            cv2.circle(clean_view, (cx, cy), r + 2, color, 2, cv2.LINE_AA)
            cv2.circle(overlay, (cx, cy), 2, color, -1, cv2.LINE_AA)

        # Annotate Zone Labels with sleek background badges
        font = cv2.FONT_HERSHEY_SIMPLEX
        fx, fy, fw, fh = rois.face_box

        # T-Zone Label
        cv2.putText(overlay, "T-ZONE (SEBUM FOCUS)", (rois.forehead_roi[0], max(20, rois.forehead_roi[1] - 8)),
                    font, 0.45, (240, 200, 30), 1, cv2.LINE_AA)
        # U-Zone Label
        cv2.putText(overlay, "U-ZONE (BARRIER & ERYTHEMA)", (rois.left_cheek_roi[0], max(20, rois.left_cheek_roi[1] - 8)),
                    font, 0.45, (230, 110, 180), 1, cv2.LINE_AA)

        return clean_view, overlay

    def analyze(self, bgr_img: np.ndarray) -> SkinAnalysisResult:
        """
        Execute full computer vision skin diagnostics on an input image.
        """
        # Ensure image has valid dimensions
        h, w = bgr_img.shape[:2]
        if h > 1200 or w > 1200:
            scale = 1000.0 / max(h, w)
            bgr_img = cv2.resize(bgr_img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

        # 1. Segment ROIs
        rois = self.roi_segmenter.segment_rois(bgr_img)
        full_face_mask = cv2.bitwise_or(rois.t_zone_mask, rois.u_zone_mask)

        # 2. Sebum & Shine
        sebum_res = self.sebum_analyzer.analyze(
            bgr_img,
            rois.t_zone_mask,
            rois.u_zone_mask,
            rois.skin_mask
        )

        # 3. Erythema in CIE-Lab
        erythema_res = self.erythema_analyzer.compute_erythema_index(
            bgr_img,
            full_face_mask
        )

        # 4. Texture and Blemish
        texture_res = self.texture_analyzer.analyze(
            bgr_img,
            full_face_mask
        )

        # 5. Composite Skin Health Index (0 to 100, where 100 is pristine calm balanced skin)
        # Penalties:
        # Sebum deviation from 0.15 balanced optimum
        sebum_penalty = abs(sebum_res.overall_sebum_score - 0.15) * 35.0
        erythema_penalty = erythema_res.erythema_index * 45.0
        texture_penalty = texture_res.roughness_score * 25.0
        blemish_penalty = min(30.0, texture_res.active_blemish_count * 2.5)

        total_penalty = sebum_penalty + erythema_penalty + texture_penalty + blemish_penalty
        health_index = int(max(15, min(98, round(100.0 - total_penalty))))

        # 6. Primary CV Concern
        if texture_res.active_blemish_count >= 6:
            primary_concern = "Active Breakouts & Inflammation"
        elif erythema_res.erythema_index > 0.40:
            primary_concern = "Vascular Erythema & Reactive Flushing"
        elif sebum_res.overall_sebum_score > 0.45:
            primary_concern = "Hyperseborrhea & Lipid Overproduction"
        elif texture_res.roughness_score > 0.50:
            primary_concern = "Surface Texture Roughness & Congestion"
        elif sebum_res.overall_sebum_score < 0.12:
            primary_concern = "Alipic Dryness & Dehydration"
        else:
            primary_concern = "Balanced Maintenance & Photoprotection"

        # 7. Render Overlays
        clean_overlay, annotated_overlay = self.render_overlay(
            bgr_img, rois, sebum_res, erythema_res, texture_res
        )

        return SkinAnalysisResult(
            sebum=sebum_res,
            erythema=erythema_res,
            texture=texture_res,
            rois=rois,
            skin_health_index=health_index,
            primary_cv_concern=primary_concern,
            diagnostic_overlay_bgr=clean_overlay,
            annotated_overlay_bgr=annotated_overlay,
            raw_image_bgr=bgr_img
        )

"""
Face Region of Interest (ROI) Segmentation: T-Zone & U-Zone extraction.
Utilizes MediaPipe / OpenCV Cascade with anthropometric facial proportion mapping.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np


@dataclass
class FacialROIs:
    """Encapsulates segmented facial regions of interest and coordinates."""
    face_box: Tuple[int, int, int, int]  # (x, y, w, h)
    t_zone_mask: np.ndarray             # Binary mask for T-Zone
    u_zone_mask: np.ndarray             # Binary mask for U-Zone
    skin_mask: np.ndarray               # General skin color mask
    forehead_roi: Tuple[int, int, int, int]
    nose_roi: Tuple[int, int, int, int]
    left_cheek_roi: Tuple[int, int, int, int]
    right_cheek_roi: Tuple[int, int, int, int]
    chin_roi: Tuple[int, int, int, int]
    t_zone_polygons: List[np.ndarray]
    u_zone_polygons: List[np.ndarray]
    landmarks: Optional[np.ndarray] = None


class FaceROISegmenter:
    """
    Robust Face and ROI Segmenter.
    Extracts T-Zone (Forehead, Nose Bridge, Philtrum) and U-Zone (Cheeks, Chin)
    using anthropometrically calibrated geometry and skin chrominance masking.
    """

    def __init__(self):
        import os
        cascade_path = getattr(cv2.data, "haarcascades", "") + "haarcascade_frontalface_default.xml"
        self.face_cascade = None
        if os.path.exists(cascade_path):
            try:
                clf = cv2.CascadeClassifier(cascade_path)
                if not clf.empty():
                    self.face_cascade = clf
            except Exception:
                self.face_cascade = None

    def extract_skin_mask(self, bgr_img: np.ndarray) -> np.ndarray:
        """
        Segment dermis pixels using combined YCrCb and HSV skin locus thresholding.
        Reduces background, clothing, and hair artifacts.
        """
        # YCrCb skin range
        ycrcb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2YCrCb)
        ycrcb_mask = cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 175, 127]))

        # HSV skin range (hue 0-25 or 170-180 for diverse Fitzpatrick tones)
        hsv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        hsv_mask1 = cv2.inRange(hsv, np.array([0, 20, 40]), np.array([25, 255, 255]))
        hsv_mask2 = cv2.inRange(hsv, np.array([170, 20, 40]), np.array([180, 255, 255]))
        hsv_mask = cv2.bitwise_or(hsv_mask1, hsv_mask2)

        # Intersect masks & clean noise with morphological opening
        combined = cv2.bitwise_and(ycrcb_mask, hsv_mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cleaned = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel, iterations=1)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=1)
        return cleaned

    def detect_face(self, bgr_img: np.ndarray) -> Tuple[int, int, int, int]:
        """
        Detect primary face bounding box. Uses cascade if available,
        skin locus contour segmentation as primary/secondary fallback,
        and centered portrait crop as tertiary fallback.
        """
        h, w = bgr_img.shape[:2]

        # 1. Try Haar cascade if available
        if self.face_cascade is not None:
            try:
                gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=4,
                    minSize=(int(w * 0.2), int(h * 0.2))
                )
                if len(faces) > 0:
                    largest_face = max(faces, key=lambda f: f[2] * f[3])
                    return tuple(int(x) for x in largest_face)
            except Exception:
                pass

        # 2. Skin chrominance contour segmentation
        skin_mask = self.extract_skin_mask(bgr_img)
        contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_cnt = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_cnt) > (h * w * 0.05):
                bx, by, bw, bh = cv2.boundingRect(largest_cnt)
                # Restrict to upper 80% to exclude excessive neck/chest
                bh = int(bh * 0.85)
                return (bx, by, bw, bh)

        # 3. Anthropometric portrait center crop
        fx = int(w * 0.15)
        fy = int(h * 0.10)
        fw = int(w * 0.70)
        fh = int(h * 0.80)
        return (fx, fy, fw, fh)

    def segment_rois(self, bgr_img: np.ndarray) -> FacialROIs:
        """
        Segment T-Zone and U-Zone ROIs from a facial image.
        Returns FacialROIs containing bounding boxes, binary masks, and polygon sets.
        """
        h_img, w_img = bgr_img.shape[:2]
        fx, fy, fw, fh = self.detect_face(bgr_img)

        # Ensure bounds stay within image dimensions
        fx = max(0, fx)
        fy = max(0, fy)
        fw = min(fw, w_img - fx)
        fh = min(fh, h_img - fy)

        # Anthropometric facial subdivision ratios:
        # Forehead (upper T-Zone): Top 8% to 32% of face, center 60% width
        forehead_x = fx + int(fw * 0.20)
        forehead_y = fy + int(fh * 0.08)
        forehead_w = int(fw * 0.60)
        forehead_h = int(fh * 0.24)

        # Nose bridge and tip (vertical bar of T-Zone): 32% to 66% of face, center 28% width
        nose_x = fx + int(fw * 0.36)
        nose_y = fy + int(fh * 0.32)
        nose_w = int(fw * 0.28)
        nose_h = int(fh * 0.34)

        # Left Cheek (U-Zone): 38% to 68% of face height, 8% to 34% width
        l_cheek_x = fx + int(fw * 0.08)
        l_cheek_y = fy + int(fh * 0.38)
        l_cheek_w = int(fw * 0.26)
        l_cheek_h = int(fh * 0.30)

        # Right Cheek (U-Zone): 38% to 68% of face height, 66% to 92% width
        r_cheek_x = fx + int(fw * 0.66)
        r_cheek_y = fy + int(fh * 0.38)
        r_cheek_w = int(fw * 0.26)
        r_cheek_h = int(fh * 0.30)

        # Chin (U-Zone base): 74% to 94% of face height, 28% to 72% width
        chin_x = fx + int(fw * 0.28)
        chin_y = fy + int(fh * 0.74)
        chin_w = int(fw * 0.44)
        chin_h = int(fh * 0.20)

        # Create full-resolution binary masks
        t_mask = np.zeros((h_img, w_img), dtype=np.uint8)
        u_mask = np.zeros((h_img, w_img), dtype=np.uint8)

        # Polygons for sleek UI visual overlays
        forehead_pts = np.array([
            [forehead_x, forehead_y],
            [forehead_x + forehead_w, forehead_y],
            [forehead_x + forehead_w, forehead_y + forehead_h],
            [forehead_x, forehead_y + forehead_h]
        ], dtype=np.int32)

        nose_pts = np.array([
            [nose_x, nose_y],
            [nose_x + nose_w, nose_y],
            [nose_x + nose_w, nose_y + nose_h],
            [nose_x, nose_y + nose_h]
        ], dtype=np.int32)

        l_cheek_pts = np.array([
            [l_cheek_x, l_cheek_y],
            [l_cheek_x + l_cheek_w, l_cheek_y],
            [l_cheek_x + l_cheek_w, l_cheek_y + l_cheek_h],
            [l_cheek_x, l_cheek_y + l_cheek_h]
        ], dtype=np.int32)

        r_cheek_pts = np.array([
            [r_cheek_x, r_cheek_y],
            [r_cheek_x + r_cheek_w, r_cheek_y],
            [r_cheek_x + r_cheek_w, r_cheek_y + r_cheek_h],
            [r_cheek_x, r_cheek_y + r_cheek_h]
        ], dtype=np.int32)

        chin_pts = np.array([
            [chin_x, chin_y],
            [chin_x + chin_w, chin_y],
            [chin_x + chin_w, chin_y + chin_h],
            [chin_x, chin_y + chin_h]
        ], dtype=np.int32)

        # Fill masks
        cv2.fillConvexPoly(t_mask, forehead_pts, 255)
        cv2.fillConvexPoly(t_mask, nose_pts, 255)
        cv2.fillConvexPoly(u_mask, l_cheek_pts, 255)
        cv2.fillConvexPoly(u_mask, r_cheek_pts, 255)
        cv2.fillConvexPoly(u_mask, chin_pts, 255)

        skin_mask = self.extract_skin_mask(bgr_img)

        # Refine ROI masks with skin locus intersection if skin pixels detected
        if np.count_nonzero(skin_mask) > 100:
            t_refined = cv2.bitwise_and(t_mask, skin_mask)
            u_refined = cv2.bitwise_and(u_mask, skin_mask)
            # Retain original mask if skin filtering is too aggressive
            if np.count_nonzero(t_refined) > 50:
                t_mask = t_refined
            if np.count_nonzero(u_refined) > 50:
                u_mask = u_refined

        return FacialROIs(
            face_box=(fx, fy, fw, fh),
            t_zone_mask=t_mask,
            u_zone_mask=u_mask,
            skin_mask=skin_mask,
            forehead_roi=(forehead_x, forehead_y, forehead_w, forehead_h),
            nose_roi=(nose_x, nose_y, nose_w, nose_h),
            left_cheek_roi=(l_cheek_x, l_cheek_y, l_cheek_w, l_cheek_h),
            right_cheek_roi=(r_cheek_x, r_cheek_y, r_cheek_w, r_cheek_h),
            chin_roi=(chin_x, chin_y, chin_w, chin_h),
            t_zone_polygons=[forehead_pts, nose_pts],
            u_zone_polygons=[l_cheek_pts, r_cheek_pts, chin_pts]
        )

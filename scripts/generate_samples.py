"""
Generate 4 clinical synthetic facial portraits for one-click testing in SkinnAlgo.
"""

import os
import cv2
import numpy as np


def create_base_portrait(w=640, h=720, skin_bgr=(165, 195, 230), bg_bgr=(245, 248, 252)):
    """Creates a base human portrait with realistic facial geometry and landmarks."""
    img = np.full((h, w, 3), bg_bgr, dtype=np.uint8)

    # Ambient vignette
    y_coords, x_coords = np.ogrid[:h, :w]
    dist_from_center = np.sqrt(((x_coords - w // 2) / (w // 2)) ** 2 + ((y_coords - h // 2) / (h // 2)) ** 2)
    vignette = np.clip(1.0 - dist_from_center * 0.35, 0.4, 1.0)
    img = (img * vignette[:, :, None]).astype(np.uint8)

    # Neck
    cv2.fillPoly(img, [np.array([[240, 480], [400, 480], [430, 720], [210, 720]])], (int(skin_bgr[0]*0.88), int(skin_bgr[1]*0.88), int(skin_bgr[2]*0.88)))

    # Face Oval
    face_center = (w // 2, int(h * 0.46))
    face_axes = (165, 215)
    cv2.ellipse(img, face_center, face_axes, 0, 0, 360, skin_bgr, -1, cv2.LINE_AA)

    # Subtle 3D shading on jaw and temples
    shading_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(shading_mask, face_center, face_axes, 0, 0, 360, 255, -1)
    inner_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(inner_mask, face_center, (145, 190), 0, 0, 360, 255, -1)
    rim_mask = cv2.subtract(shading_mask, inner_mask)
    img[rim_mask > 0] = (img[rim_mask > 0] * 0.90).astype(np.uint8)

    # Eyebrows
    eyebrow_color = (40, 40, 50)
    # Left brow
    cv2.ellipse(img, (250, 255), (38, 12), -8, 200, 350, eyebrow_color, 4, cv2.LINE_AA)
    # Right brow
    cv2.ellipse(img, (390, 255), (38, 12), 8, 190, 340, eyebrow_color, 4, cv2.LINE_AA)

    # Eyes
    eye_white = (240, 240, 245)
    iris_color = (55, 65, 80)
    # Left eye
    cv2.ellipse(img, (250, 285), (24, 12), 0, 0, 360, eye_white, -1, cv2.LINE_AA)
    cv2.circle(img, (250, 285), 9, iris_color, -1, cv2.LINE_AA)
    cv2.circle(img, (250, 285), 4, (15, 15, 20), -1, cv2.LINE_AA)
    cv2.ellipse(img, (250, 285), (25, 13), 0, 0, 360, (70, 75, 85), 2, cv2.LINE_AA)
    # Right eye
    cv2.ellipse(img, (390, 285), (24, 12), 0, 0, 360, eye_white, -1, cv2.LINE_AA)
    cv2.circle(img, (390, 285), 9, iris_color, -1, cv2.LINE_AA)
    cv2.circle(img, (390, 285), 4, (15, 15, 20), -1, cv2.LINE_AA)
    cv2.ellipse(img, (390, 285), (25, 13), 0, 0, 360, (70, 75, 85), 2, cv2.LINE_AA)

    # Nose
    nose_color = (int(skin_bgr[0]*0.80), int(skin_bgr[1]*0.80), int(skin_bgr[2]*0.80))
    cv2.line(img, (320, 280), (320, 375), nose_color, 3, cv2.LINE_AA)
    # Nose bulb and alar creases
    cv2.ellipse(img, (320, 375), (18, 10), 0, 0, 360, nose_color, -1, cv2.LINE_AA)
    cv2.circle(img, (306, 380), 5, (int(skin_bgr[0]*0.72), int(skin_bgr[1]*0.72), int(skin_bgr[2]*0.72)), -1)
    cv2.circle(img, (334, 380), 5, (int(skin_bgr[0]*0.72), int(skin_bgr[1]*0.72), int(skin_bgr[2]*0.72)), -1)

    # Lips
    lip_color = (130, 140, 195)
    # Upper lip
    cv2.ellipse(img, (320, 440), (36, 12), 0, 180, 360, lip_color, -1, cv2.LINE_AA)
    # Lower lip
    cv2.ellipse(img, (320, 442), (32, 14), 0, 0, 180, (140, 150, 205), -1, cv2.LINE_AA)
    cv2.line(img, (285, 441), (355, 441), (90, 95, 150), 2, cv2.LINE_AA)

    # Hair silhouette
    hair_color = (30, 30, 38)
    cv2.ellipse(img, (w // 2, 175), (175, 85), 0, 180, 360, hair_color, -1, cv2.LINE_AA)
    cv2.ellipse(img, (165, 290), (35, 110), 0, 0, 360, hair_color, -1, cv2.LINE_AA)
    cv2.ellipse(img, (475, 290), (35, 110), 0, 0, 360, hair_color, -1, cv2.LINE_AA)

    return img


def generate_sample_profiles():
    os.makedirs("assets/samples", exist_ok=True)

    # 1. OILY & ACNE PROFILE
    img1 = create_base_portrait(skin_bgr=(160, 190, 225))
    # Specular shine on forehead and nose
    shine_color = (255, 255, 255)
    cv2.ellipse(img1, (320, 205), (55, 25), 0, 0, 360, shine_color, -1)
    cv2.ellipse(img1, (320, 345), (15, 30), 0, 0, 360, shine_color, -1)
    cv2.ellipse(img1, (320, 375), (12, 10), 0, 0, 360, shine_color, -1)
    # Blur shine to create natural gloss
    img1 = cv2.GaussianBlur(img1, (7, 7), 0)

    # Inflammatory papules and pustules (Rose Red rings with whitish/yellowish centers)
    acne_spots = [
        (310, 190, 7), (335, 215, 8), (280, 225, 6),
        (315, 335, 7), (325, 360, 6),
        (235, 340, 9), (245, 370, 8), (220, 360, 6),
        (395, 345, 8), (410, 380, 9), (380, 365, 7),
        (320, 485, 8), (305, 500, 6)
    ]
    for x, y, r in acne_spots:
        # Erythematous flare halo
        cv2.circle(img1, (x, y), r + 5, (90, 100, 215), -1, cv2.LINE_AA)
        # Inflamed papule core
        cv2.circle(img1, (x, y), r, (70, 75, 235), -1, cv2.LINE_AA)
        # Pustule micro-center
        cv2.circle(img1, (x, y), max(2, r - 4), (160, 220, 245), -1, cv2.LINE_AA)

    # Micro texture noise
    noise = np.random.normal(0, 5, img1.shape).astype(np.int16)
    img1 = np.clip(img1.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    cv2.imwrite("assets/samples/oily_acne_profile.png", img1)

    # 2. DRY & ERYTHEMA (ROSACEA / BARRIER) PROFILE
    img2 = create_base_portrait(skin_bgr=(170, 195, 235))
    # Marked diffuse flushing over cheeks and nose (elevated a* redness)
    # Left cheek flush
    cv2.ellipse(img2, (245, 360), (45, 35), -15, 0, 360, (110, 115, 235), -1)
    # Right cheek flush
    cv2.ellipse(img2, (395, 360), (45, 35), 15, 0, 360, (110, 115, 235), -1)
    # Nose bridge flush
    cv2.ellipse(img2, (320, 350), (22, 30), 0, 0, 360, (120, 125, 230), -1)
    # Chin flush
    cv2.ellipse(img2, (320, 490), (25, 18), 0, 0, 360, (120, 125, 225), -1)
    # Smooth blend flush
    img2 = cv2.GaussianBlur(img2, (15, 15), 0)
    cv2.imwrite("assets/samples/dry_erythema_profile.png", img2)

    # 3. COMBINATION & HYPERPIGMENTATION PROFILE
    img3 = create_base_portrait(skin_bgr=(145, 175, 215))
    # Moderate shine strictly on forehead and nose
    cv2.ellipse(img3, (320, 210), (45, 20), 0, 0, 360, (245, 245, 245), -1)
    cv2.ellipse(img3, (320, 350), (12, 25), 0, 0, 360, (240, 240, 240), -1)
    img3 = cv2.GaussianBlur(img3, (9, 9), 0)
    # Melasma / PIH dark macules on lateral cheeks and forehead
    spots = [
        (225, 320, 12), (240, 340, 9), (215, 360, 14), (255, 330, 8),
        (410, 325, 11), (395, 350, 13), (425, 360, 10),
        (275, 210, 10), (360, 215, 12)
    ]
    for x, y, r in spots:
        cv2.circle(img3, (x, y), r, (90, 115, 150), -1, cv2.LINE_AA)
    img3 = cv2.GaussianBlur(img3, (5, 5), 0)
    cv2.imwrite("assets/samples/combo_pigment_profile.png", img3)

    # 4. BALANCED EUDERMIC PROFILE
    img4 = create_base_portrait(skin_bgr=(170, 200, 235))
    # Soft, diffuse radiant glow without specular hotspot
    cv2.ellipse(img4, (320, 210), (35, 15), 0, 0, 360, (210, 230, 250), -1)
    cv2.ellipse(img4, (320, 355), (10, 18), 0, 0, 360, (210, 230, 250), -1)
    img4 = cv2.GaussianBlur(img4, (11, 11), 0)
    cv2.imwrite("assets/samples/balanced_profile.png", img4)

    print("Successfully generated 4 clinical profile sample images in assets/samples/")


if __name__ == "__main__":
    generate_sample_profiles()


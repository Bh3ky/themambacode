# src/core/preprocess.py

# Responsible for converting raw images into a stable brightness map.

import cv2
import numpy as np

def preprocess_image(
    image_path: str,
    target_width: int,
    target_height: int,
    gamma: float) -> np.ndarray:
    """
    Load and preprocess image for halftone generation.
    Return normalised grayscale brightness map [0, 1]
    Improved for better shade accuracy and detail preservation.
    """

    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or could not be loaded.")
    
    # Resize to target dimensations (portrait)
    img = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)

    # Convert to grayscale using perceptual luminance weights
    # This better matches human perception of brightness
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE for better local contrast (adaptive histogram equalization)
    # Balanced clipLimit for good contrast without over-processing
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Normalise to [0, 1]
    gray = gray.astype(np.float32) / 255.0

    # Gamma correction for contrast control
    gray = np.power(gray, gamma)

    # Subtle edge enhancement for definition without artifacts
    edges = cv2.Canny((gray * 255).astype(np.uint8), 50, 150)
    edges = edges.astype(np.float32) / 255.0
    gray = np.clip(gray - edges * 0.06, 0, 1)

    # Normalize to maximize dynamic range without being too aggressive
    gray_min = np.percentile(gray, 1)
    gray_max = np.percentile(gray, 99)
    if gray_max - gray_min > 0.05:
        gray = np.clip((gray - gray_min) / (gray_max - gray_min), 0.0, 1.0)
    
    # Single, balanced S-curve for natural contrast enhancement
    # This preserves detail while enhancing shadows for feature visibility
    gray = np.power(gray, 0.95)  # Gentle compression in highlights
    gray = 1.0 - np.power(1.0 - gray, 1.05)  # Gentle expansion in shadows

    return gray

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
    """

    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or could not be loaded.")
    
    # Resize to target dimensations (portrait)
    img = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE for better local contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Normalise to [0, 1]
    gray = gray.astype(np.float32) / 255.0

    # Gamma correction for contrast control
    gray = np.power(gray, gamma)

    # Edge enhancement (subtle)
    edges = cv2.Canny((gray * 255).astype(np.uint8), 50, 150)
    edges = edges.astype(np.float32) / 255.0
    gray = np.clip(gray - edges * 0.15, 0, 1)

    return gray

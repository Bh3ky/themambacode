# src/core/preprocess.py

# Responsible for converting raw images into a stable brightness map.

import cv2
import numpy as np
from config import TARGET_WIDTH, GAMMMA

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load image, normalise contrast, and return grayscale
    values in range [0, 1]
    """

    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or could not be loaded.")
    
    # Resize while keeping aspect ratio
    h, w = img.shape[:2]
    scale = TARGET_WIDTH / w
    img = cv2.resize(img, (TARGET_WIDTH, int(h * scale)))

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Normalise to [0, 1]
    gray = gray.astype(np.float32) / 255.0

    # Gamma correction (contrast sculpting)
    gray = np.power(gray, GAMMMA)

    return gray

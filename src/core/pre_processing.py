# src/core/preprocess.py

# Responsible for converting raw images into a stable brightness map.

import cv2
import numpy as np

def preprocess_image(
    image_path: str,
    target_width: int,
    target_height: int,
    gamma: float = 1.0,
    enhanced_contrast: bool = False) -> np.ndarray:
    """
    Load and preprocess image for halftone generation.
    Return normalised grayscale brightness map [0, 1]

    Args: 
        image_path: Path to the input image
        target_width: Target width in pixels
        target_height: Target height in pixels
        gamma: Gamma correction value (1.0 = no correction, <1 = darker, >1 = brighter)
        enhanced_contrast: Apply CLAHE for local contrast enhancement

    Returns:
        Normalised brightness map where 0 = black, 1 = white
    """

    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or could not be loaded.")
    
    # Resize to target dimensations (portrait)
    img = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)

    # Convert to grayscale using perceptual luminance weights
    # OpenCV uses: Y = 0.299*R + 0.587*G + 0.114*B
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Optional: Apply CLAHE for local contrast enhancement
    # Only use this if the source image is flat/low-contrast
    if enhanced_contrast:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)

    # Normalise to [0, 1] float range
    gray = gray.astype(np.float32) / 255.0

    # Apply gamma correction for overall contrast control
    # gamma < 1.0: darkens midtones (more contrast)
    # gamma > 1.0: lightens midtones (less contrast)
    # gamma = 1.0: no change
    if gamma != 1.0:
        gray = np.power(gray, gamma)
    

    # Optional: Normalise to use full dynamic range
    # Ensures blacks are truly black and whites are truly white
    # Use percentiles to avoid outliers affect the normalisation
    gray_min = np.percentile(gray, 1)
    gray_max = np.percentile(gray, 99)

    if gray_max - gray_min > 0.05:
        gray = np.clip((gray - gray_min) / (gray_max - gray_min), 0.0, 1.0)
        
    return gray 


def preprocess_image_advanced(
    image_path: str,
    target_width: int,
    target_height: int,
    gamma: float = 1.0,
    contrast_enhancement: bool = False,
    edge_enhancement: bool = False
    ) -> np.ndarray:
    """
    Advanced preprocessing with optional edge enhancement.
    Use case: ONLY after getting basic halftone working.

    Args:
        image_path: Path to input image
        target_width: Target width in pixels
        target_height: Target height in pixels
        gamma: Gamma correction (1.0 = neutral)
        contrast_enhancement: CLAHE strength (0.0 = off, 1.0-3.0 = light-strong)
        edge_enhancement: Edge darkening strength (0.0 = off, 0.05-0.15 = light-strong)
    
    Returns:
        Normalized brightness map [0, 1]
    """
    
    # Load and resize
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found: {image_path}")
    
    img = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply CLAHE if requested
    if contrast_enhancement > 0.0:
        clahe = cv2.createCLAHE(
            clipLimit=contrast_enhancement, 
            tileGridSize=(8, 8)
        )
        gray = clahe.apply(gray)
    
    # Normalize to float
    gray = gray.astype(np.float32) / 255.0
    
    # Apply gamma correction
    if gamma != 1.0:
        gray = np.power(gray, gamma)
    


    if edge_enhancement > 0.0:
        # Detect edges
        edges = cv2.Canny(
            (gray * 255).astype(np.uint8), 
            threshold1=50, 
            threshold2=150
        )
        edges = edges.astype(np.float32) / 255.0
        
        # Darken edge regions
        gray = np.clip(gray - edges * edge_enhancement, 0.0, 1.0)
    
    # Normalize dynamic range
    gray_min = np.percentile(gray, 1)
    gray_max = np.percentile(gray, 99)
    
    if gray_max - gray_min > 0.1:
        gray = np.clip((gray - gray_min) / (gray_max - gray_min), 0.0, 1.0)
    
    return gray
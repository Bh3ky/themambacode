# src/core/half_tone.py

import cv2
import numpy as np
from PIL import Image, ImageDraw
from typing import Dict, Tuple


def generate_classic_halftone(
    brightness_map: np.ndarray,
    config: Dict,
    bg_color: Tuple[int, int, int],
    dot_color: Tuple[int, int, int]) -> Image.Image:
    """
    Generate a classic dot halftone image from brightness map.
    Improved shade accuracy with non-linear brightness mapping and adaptive sampling.
    """

    height, width = brightness_map.shape
    cell_size = int(config["cell_size"])
    max_radius = config["max_radius"]
    threshold = config["brightness_threshold"]

    # Normalize brightness map for good dynamic range
    # Balanced approach - not too aggressive
    brightness_min = np.percentile(brightness_map, 2)
    brightness_max = np.percentile(brightness_map, 98)
    brightness_range = brightness_max - brightness_min
    if brightness_range > 0.01:
        brightness_map_normalized = np.clip(
            (brightness_map - brightness_min) / brightness_range, 0.0, 1.0
        )
    else:
        brightness_map_normalized = brightness_map

    # Create black canvas
    canvas = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(canvas)

    # Loop over sampling grid
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):

            # extract cell
            cell = brightness_map_normalized[y:y+cell_size, x:x+cell_size]
            if cell.size == 0:
                continue

            # Use median for more robust brightness estimation (less sensitive to outliers)
            # Weighted towards center of cell for better detail preservation
            cell_center_y = cell_size // 2
            cell_center_x = cell_size // 2
            weights = np.zeros_like(cell, dtype=np.float32)
            for i in range(cell.shape[0]):
                for j in range(cell.shape[1]):
                    # Gaussian-like weighting: center pixels have more influence
                    dist = np.sqrt((i - cell_center_y)**2 + (j - cell_center_x)**2)
                    weights[i, j] = np.exp(-dist**2 / (2 * (cell_size / 3)**2))
            
            # Weighted average with fallback to median
            if weights.sum() > 0:
                brightness = float(np.average(cell, weights=weights))
            else:
                brightness = float(np.median(cell))

            # Threshold handling - skip very bright areas
            if brightness > threshold:
                continue

            # Non-linear brightness-to-radius mapping
            # Invert brightness: darker areas = larger dots
            brightness_inverted = 1.0 - brightness
            
            # Balanced gamma correction for natural dot size distribution
            # This ensures good representation across all tone ranges
            gamma_correction = 0.65  # Balanced for natural halftone effect
            brightness_corrected = np.power(brightness_inverted, gamma_correction)
            
            # Map to radius with smooth curve
            radius = max_radius * brightness_corrected
            
            # Minimum radius to avoid tiny dots that don't contribute
            min_radius = 0.25
            if radius < min_radius:
                continue

            # Dot center
            cx = x + cell_size // 2
            cy = y + cell_size // 2

            # draw dot
            draw.ellipse(
                (
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius,
                ),
                fill=dot_color
            )
    
    return canvas

def generate_line_halftone(
    brightness_map: np.ndarray,
    config: Dict,
    bg_color: Tuple[int, int, int],
    line_color: Tuple[int, int, int]
) -> Image.Image:
    """
    Generate fingerprint-style contour line halftone.
    """
    height, width = brightness_map.shape
    canvas = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(canvas)
    
    # Create contour lines based on brightness levels
    line_spacing = config["cell_size"]
    
    for brightness_level in np.arange(0.1, 0.9, 0.05):
        # Find contours at this brightness level
        mask = ((brightness_map >= brightness_level - 0.025) & 
                (brightness_map <= brightness_level + 0.025))
        mask = mask.astype(np.uint8) * 255
        
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if len(contour) > 10:  # Filter small contours
                contour = contour.reshape(-1, 2)
                points = [(int(x), int(y)) for [[x, y]] in contour]
                if len(points) > 2:
                    # Vary line width based on brightness
                    width = max(1, int(3 * (1 - brightness_level)))
                    draw.line(points, fill=line_color, width=width)
    
    return canvas
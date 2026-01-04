# src/core/half_tone.py

"""
Halftone generation functions.
Creates dot-based halftone images from brightness maps.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw
from typing import Dict, Tuple


def generate_classic_halftone(
    brightness_map: np.ndarray,
    config: Dict,
    bg_color: Tuple[int, int, int],
    dot_color: Tuple[int, int, int]
) -> Image.Image:
    """
    Generate classic circular dot halftone.
    
    How it works:
    1. Divide image into grid cells
    2. Sample brightness in each cell
    3. Draw dots sized inversely to brightness
        - Bright areas → small/no dots (white background shows through)
        - Dark areas → large dots (cover the white background)
    
    Args:
        brightness_map: Normalized grayscale image [0=black, 1=white]
        config: Dict with 'cell_size' and 'max_radius'
        bg_color: Background color RGB tuple
        dot_color: Dot color RGB tuple
    
    Returns:
        PIL Image with halftone effect
    """
    
    height, width = brightness_map.shape
    cell_size = int(config["cell_size"])
    max_radius = float(config["max_radius"])
    
    # Create canvas with background color
    canvas = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(canvas)
    
    # Process grid of cells
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            
            # Extract cell region
            cell = brightness_map[y:y+cell_size, x:x+cell_size]
            if cell.size == 0:
                continue
            
            # Calculate average brightness of this cell
            # brightness: 0 = black/dark, 1 = white/bright
            brightness = float(np.mean(cell))
            
            # Convert brightness to dot size
            # For halftone: bright areas need small dots, dark areas need large dots
            # So we invert: dot_intensity = 1 - brightness
            dot_intensity = 1.0 - brightness
            
            # Apply gamma curve for better dot distribution
            # gamma < 1.0: emphasizes shadows (larger range of small dots)
            # gamma > 1.0: emphasizes highlights (larger range of big dots)
            # gamma = 1.0: linear mapping
            gamma = 0.7  # Slightly emphasize shadows for better detail
            dot_intensity = np.power(dot_intensity, gamma)
            
            # Calculate dot radius
            radius = max_radius * dot_intensity
            
            # Skip very small dots (they don't contribute visually)
            # This also naturally handles very bright areas
            min_radius = 0.6
            if radius < min_radius:
                continue
            
            # Calculate dot center (center of cell)
            cx = x + cell_size // 2
            cy = y + cell_size // 2
            
            # Draw circular dot
            draw.ellipse(
                (
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius
                ),
                fill=dot_color
            )
    
    return canvas


def generate_variable_halftone(
    brightness_map: np.ndarray,
    config: Dict,
    bg_color: Tuple[int, int, int],
    dot_color: Tuple[int, int, int],
    dot_gamma: float = 0.7,
    angle: float = 0.0
) -> Image.Image:
    """
    Advanced halftone with configurable gamma and rotation.
    
    Args:
        brightness_map: Normalized grayscale [0, 1]
        config: Dict with 'cell_size' and 'max_radius'
        bg_color: Background RGB
        dot_color: Dot RGB
        dot_gamma: Gamma for dot size distribution (0.5-1.5)
        angle: Rotation angle in degrees (0, 15, 45, etc.)
    
    Returns:
        PIL Image with halftone
    """
    
    height, width = brightness_map.shape
    cell_size = int(config["cell_size"])
    max_radius = float(config["max_radius"])
    
    # Rotate brightness map if angle specified
    if angle != 0.0:
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        brightness_map = cv2.warpAffine(
            brightness_map, 
            rotation_matrix, 
            (width, height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REPLICATE
        )
    
    canvas = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(canvas)
    
    # Generate dots
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            
            cell = brightness_map[y:y+cell_size, x:x+cell_size]
            if cell.size == 0:
                continue
            
            brightness = float(np.mean(cell.astype(np.float64)))
            dot_intensity = 1.0 - brightness
            
            # Apply custom gamma
            dot_intensity = np.power(dot_intensity, dot_gamma)
            
            radius = max_radius * dot_intensity
            
            if radius < 0.6:
                continue
            
            cx = x + cell_size // 2
            cy = y + cell_size // 2
            
            draw.ellipse(
                (cx - radius, cy - radius, cx + radius, cy + radius),
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
    Generate contour line halftone (fingerprint style).
    
    Creates lines at different brightness levels to simulate
    topographic contours or fingerprint ridges.
    
    Args:
        brightness_map: Normalized grayscale [0, 1]
        config: Dict with 'cell_size' (used as line spacing)
        bg_color: Background RGB
        line_color: Line RGB
    
    Returns:
        PIL Image with line halftone
    """
    
    height, width = brightness_map.shape
    canvas = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(canvas)
    
    # Convert brightness map to uint8 for contour detection
    brightness_uint8 = (brightness_map * 255).astype(np.uint8)
    
    # Generate contours at different brightness levels
    # More levels = more detailed effect
    num_levels = 15
    for i in range(num_levels):
        # Calculate brightness threshold for this level
        brightness_level = (i + 1) / (num_levels + 1)
        threshold = int(brightness_level * 255)
        
        # Create binary mask at this threshold
        _, mask = cv2.threshold(
            brightness_uint8, 
            threshold, 
            255, 
            cv2.THRESH_BINARY
        )
        
        # Find contours
        contours, _ = cv2.findContours(
            mask, 
            cv2.RETR_LIST, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Draw contours
        for contour in contours:
            if len(contour) > 10:  # Filter tiny contours
                # Convert contour points to list of tuples
                # Reshape contour from (n, 1, 2) to (n, 2) for easier access
                contour_reshaped = contour.reshape(-1, 2)
                points = [(int(pt[0]), int(pt[1])) for pt in contour_reshaped]
                
                # Vary line width based on brightness level
                # Darker levels = thicker lines
                line_width = max(1, int(4 * (1 - brightness_level)))
                
                # Draw the contour line
                if len(points) > 1:
                    draw.line(points, fill=line_color, width=line_width)
    
    return canvas


def generate_square_halftone(
    brightness_map: np.ndarray,
    config: Dict,
    bg_color: Tuple[int, int, int],
    square_color: Tuple[int, int, int]
) -> Image.Image:
    """
    Generate square dot halftone.
    Similar to classic halftone but with square dots instead of circles.
    
    Args:
        brightness_map: Normalized grayscale [0, 1]
        config: Dict with 'cell_size' and 'max_radius'
        bg_color: Background RGB
        square_color: Square RGB
    
    Returns:
        PIL Image with square halftone
    """
    
    height, width = brightness_map.shape
    cell_size = int(config["cell_size"])
    max_size = float(config["max_radius"]) * 2  # Convert radius to side length
    
    canvas = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(canvas)
    
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            
            cell = brightness_map[y:y+cell_size, x:x+cell_size]
            if cell.size == 0:
                continue
            
            brightness = float(np.mean(cell))
            dot_intensity = 1.0 - brightness
            dot_intensity = np.power(dot_intensity, 0.7)
            
            square_size = max_size * dot_intensity
            
            if square_size < 1.2:
                continue
            
            # Calculate square center
            cx = x + cell_size // 2
            cy = y + cell_size // 2
            
            # Draw square
            half_size = square_size / 2
            draw.rectangle(
                (
                    cx - half_size,
                    cy - half_size,
                    cx + half_size,
                    cy + half_size
                ),
                fill=square_color
            )
    
    return canvas

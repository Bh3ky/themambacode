# src/core/halft_tone.py

import numpy as np
from PIL import Image, ImageDraw
from config import (
    CELL_SIZE,
    MAX_DOT_RADIUS,
    BRIGHTNESS_THRESHOLD,
    BACKGROUND_COLOR,
    DOT_COLOR,
)

def generate_dot_halftone(brightness_map: np.ndarray) -> Image.Image:
    """
    Generate a classic dot halftone image from brightness map.
    """

    height, width = brightness_map.shape

    # Create black canvas
    canvas = Image.new("RGB", (width, height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(canvas)

    # Loop over sampling grid
    for y in range(0, height, CELL_SIZE):
        for x in range(0, width, CELL_SIZE):

            # extract cell
            cell = brightness_map[y:y+CELL_SIZE, x:x+CELL_SIZE]
            if cell.size == 0:
                continue

            # convert numpy scalar -> python float
            b: float = float(np.mean(cell))

            # skip highlights
            if b > BRIGHTNESS_THRESHOLD:
                continue

            # map brightness -> radius
            radius: float = float(MAX_DOT_RADIUS * (1 -b))
            if radius <= 0:
                continue

            # Dot center
            cx: float = float(x + CELL_SIZE // 2)
            cy: float = float(y + CELL_SIZE // 2)

            # draw dot
            draw.ellipse(
                (
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius,
                ),
                fill=DOT_COLOR
            )
    
    return canvas
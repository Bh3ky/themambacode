"""
Quote overlay functionality for motivational poster effect.
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Tuple


def add_quote_overlay(
    image: Image.Image,
    quote_text: str,
    color_scheme: Dict,
    quote_config: Dict
) -> Image.Image:
    """
    Add repeating quote banner overlay to image.
    
    Args:
        image: Base PIL Image
        quote_text: Text to display (will be repeated)
        color_scheme: Dict with 'quote_bg' and 'quote_text' colors
        quote_config: Dict with position, padding, font_size, repeat_count
    
    Returns:
        New PIL Image with quote overlay
    """
    
    # Create a copy to avoid modifying original
    output = image.copy()
    width, height = output.size
    
    # Extract config
    position = quote_config.get("position", "top")
    padding = quote_config.get("padding", 40)
    font_size = quote_config.get("font_size", 64)
    repeat_count = quote_config.get("repeat_count", 12)
    line_spacing = quote_config.get("line_spacing", 8)
    opacity = quote_config.get("opacity", 1.0)
    
    # Load font (try multiple common font paths)
    try:
        # Try system fonts
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                # Fallback to default
                font = ImageFont.load_default()
    
    # Create repeating text
    repeated_text = (" • " + quote_text) * repeat_count
    
    # Create temporary image for text measurement
    temp_img = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Measure text dimensions
    bbox = temp_draw.textbbox((0, 0), repeated_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate banner dimensions
    banner_height = text_height + (padding * 2)
    
    # Create semi-transparent overlay
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Draw banner background
    bg_color = color_scheme["quote_bg"]
    if opacity < 1.0:
        # Add alpha channel for transparency
        bg_color = (*bg_color, int(255 * opacity))
    
    if position == "top":
        banner_y = 0
    elif position == "bottom":
        banner_y = height - banner_height
    else:  # center
        banner_y = (height - banner_height) // 2
    
    # Draw banner rectangle
    overlay_draw.rectangle(
        [(0, banner_y), (width, banner_y + banner_height)],
        fill=bg_color
    )
    
    # Draw text (repeat to fill width)
    text_color = color_scheme["quote_text"]
    text_y = banner_y + padding
    
    # Draw text multiple times to ensure full coverage
    x_offset = 0
    while x_offset < width:
        overlay_draw.text(
            (x_offset, text_y),
            repeated_text,
            fill=text_color,
            font=font
        )
        x_offset += text_width
    
    # Composite overlay onto original image
    output = Image.alpha_composite(output.convert('RGBA'), overlay)
    
    # Convert back to RGB
    output = output.convert('RGB')
    
    return output


def add_simple_quote(
    image: Image.Image,
    quote_text: str,
    position: str = "bottom",
    font_size: int = 48,
    text_color: Tuple[int, int, int] = (255, 255, 255),
    bg_color: Tuple[int, int, int] = (0, 0, 0),
    padding: int = 30
) -> Image.Image:
    """
    Add simple centered quote without repetition.
    
    Args:
        image: Base PIL Image
        quote_text: Quote to display
        position: 'top', 'bottom', or 'center'
        font_size: Font size in points
        text_color: RGB tuple for text
        bg_color: RGB tuple for background
        padding: Padding around text
    
    Returns:
        New PIL Image with quote
    """
    
    output = image.copy()
    width, height = output.size
    draw = ImageDraw.Draw(output)
    
    # Load font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Measure text
    bbox = draw.textbbox((0, 0), quote_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position
    text_x = (width - text_width) // 2
    
    if position == "top":
        text_y = padding
    elif position == "bottom":
        text_y = height - text_height - padding
    else:  # center
        text_y = (height - text_height) // 2
    
    # Draw background rectangle
    bg_padding = 20
    draw.rectangle(
        [
            (text_x - bg_padding, text_y - bg_padding),
            (text_x + text_width + bg_padding, text_y + text_height + bg_padding)
        ],
        fill=bg_color
    )
    
    # Draw text
    draw.text((text_x, text_y), quote_text, fill=text_color, font=font)
    
    return output


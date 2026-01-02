from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Tuple

def add_quote_overlay(
    image: Image.Image,
    quote: str,
    color_scheme: Dict,
    config: Dict
) -> Image.Image:
    """
    Add Mamba Mentality quote overlay to image with natural halftone integration.
    """
    width, height = image.size
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Try to load a bold font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 
                                config["font_size"])
    except:
        try:
            # Try alternative font paths
            font = ImageFont.truetype("Arial", config["font_size"])
        except:
            font = ImageFont.load_default()
    
    # Calculate quote box dimensions
    padding = config["padding"]
    repeat_count = config["repeat_count"]
    line_spacing = config["line_spacing"]
    
    # Repeat quote for bold visual effect (like reference image)
    repeated_text = (quote + " ") * repeat_count
    
    # Position quote box at top (like reference image)
    position = config["position"]
    if position == "top":
        box_y = 0  # Start at very top
    elif position == "bottom":
        box_y = height - config["font_size"] - (2 * padding)
    else:  # center
        box_y = (height - config["font_size"] - (2 * padding)) // 2
    
    # Calculate box height - single line banner style
    box_height = config["font_size"] + (2 * padding)
    
    # Draw solid background banner (full width, like reference)
    bg_color = color_scheme["quote_bg"]
    # Use full opacity for solid banner effect - clean and bold
    draw.rectangle(
        [(0, box_y), (width, box_y + box_height)],
        fill=bg_color + (255,)  # Fully opaque for clean integration
    )
    
    # Draw text - single continuous line across banner (like reference)
    text_color = color_scheme["quote_text"]
    text_y = box_y + padding
    
    # Calculate how much text fits on one line
    # Keep repeating the quote until it fills the width
    text_x = padding
    current_text = ""
    
    # Build text that fits the width
    words = repeated_text.split()
    for word in words:
        test_text = current_text + word + " "
        bbox = draw.textbbox((0, 0), test_text, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= width - (2 * padding):
            current_text = test_text
        else:
            break
    
    # If we have space, repeat more
    if len(current_text) > 0:
        remaining_width = width - (2 * padding) - draw.textbbox((0, 0), current_text, font=font)[2]
        # Try to fit more repetitions
        while remaining_width > len(quote) * 10:  # Rough estimate
            test_repeat = current_text + quote + " "
            bbox = draw.textbbox((0, 0), test_repeat, font=font)
            if bbox[2] - bbox[0] <= width - (2 * padding):
                current_text = test_repeat
                remaining_width = width - (2 * padding) - bbox[2]
            else:
                break
    
    # Draw the text
    draw.text((padding, text_y), current_text, font=font, fill=text_color)
    
    # Composite overlay onto original image with proper blending
    result = Image.alpha_composite(image.convert("RGBA"), overlay)
    return result.convert("RGB")

from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Tuple

def add_quote_overlay(
    image: Image.Image,
    quote: str,
    color_scheme: Dict,
    config: Dict
) -> Image.Image:
    """
    Add Mamba Mentality quote overlay to image.
    """
    width, height = image.size
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Try to load a bold font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 
                                config["font_size"])
    except:
        font = ImageFont.load_default()
    
    # Calculate quote box dimensions
    padding = config["padding"]
    repeat_count = config["repeat_count"]
    line_spacing = config["line_spacing"]
    
    # Repeat quote for bold visual effect
    repeated_text = (quote + " ") * repeat_count
    
    # Wrap text to fit width
    max_width = width - (2 * padding)
    wrapped_lines = []
    words = repeated_text.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                wrapped_lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        wrapped_lines.append(current_line.strip())
    
    # Limit to reasonable number of lines
    wrapped_lines = wrapped_lines[:4]
    
    # Calculate box height
    line_height = draw.textbbox((0, 0), "A", font=font)[3] + line_spacing
    box_height = (len(wrapped_lines) * line_height) + (2 * padding)
    
    # Position quote box
    position = config["position"]
    if position == "top":
        box_y = padding
    elif position == "bottom":
        box_y = height - box_height - padding
    else:  # center
        box_y = (height - box_height) // 2
    
    # Draw semi-transparent background box
    bg_color = color_scheme["quote_bg"]
    opacity = int(config["opacity"] * 255)
    draw.rectangle(
        [(padding, box_y), (width - padding, box_y + box_height)],
        fill=bg_color + (opacity,)
    )
    
    # Draw text
    text_color = color_scheme["quote_text"]
    y_text = box_y + padding
    for line in wrapped_lines:
        draw.text((padding * 1.5, y_text), line, font=font, fill=text_color)
        y_text += line_height
    
    # Composite overlay onto original image
    result = Image.alpha_composite(image.convert("RGBA"), overlay)
    return result.convert("RGB")

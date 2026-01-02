# src/main.py

import argparse
import random
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    HALFTONE_STYLES, COLOR_SCHEMES, QUOTE_CONFIG, MAMBA_QUOTES,
    TARGET_WIDTH, TARGET_HEIGHT
)
from core.pre_processing import preprocess_image
from core.half_tone import generate_classic_halftone, generate_line_halftone
from core.quote_overlay import add_quote_overlay


def main():
    parser = argparse.ArgumentParser(
        description="Mamba Mentality Halftone Generator - Create motivational portrait art"
    )
    parser.add_argument("--input", required=True, help="Path to input image")
    parser.add_argument("--output", default="output/halftone.png", help="Output file path")
    parser.add_argument("--style", default="classic_dots", 
                    choices=list(HALFTONE_STYLES.keys()),
                    help="Halftone style")
    parser.add_argument("--color", default="classic",
                    choices=list(COLOR_SCHEMES.keys()),
                    help="Color scheme")
    parser.add_argument("--quote", default="random",
                    help="Specific quote or 'random'")
    parser.add_argument("--line-effect", action="store_true",
                    help="Use fingerprint line effect instead of dots")
    parser.add_argument("--no-quote", action="store_true",
                    help="Generate without quote overlay")
    
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load style config
    style_config = HALFTONE_STYLES[args.style]
    color_scheme = COLOR_SCHEMES[args.color]
    
    # Preprocess image
    print(f"Processing: {args.input}")
    print(f"Style: {args.style} | Color: {args.color}")
    
    brightness_map = preprocess_image(
        args.input,
        TARGET_WIDTH,
        TARGET_HEIGHT,
        style_config["gamma"]
    )
    
    # Generate halftone
    if args.line_effect:
        print("Generating fingerprint line effect...")
        halftone_img = generate_line_halftone(
            brightness_map,
            style_config,
            color_scheme["background"],
            color_scheme["dots"]
        )
    else:
        print("Generating classic dot halftone...")
        halftone_img = generate_classic_halftone(
            brightness_map,
            style_config,
            color_scheme["background"],
            color_scheme["dots"]
        )
    
    # Add quote overlay
    if not args.no_quote:
        if args.quote == "random":
            quote = random.choice(MAMBA_QUOTES)
        else:
            quote = args.quote.upper()
        
        print(f"Adding quote: {quote[:50]}...")
        halftone_img = add_quote_overlay(
            halftone_img,
            quote,
            color_scheme,
            QUOTE_CONFIG
        )
    
    # Save
    halftone_img.save(args.output, quality=95, dpi=(300, 300))
    print(f"✓ Saved: {args.output}")
    print(f"  Dimensions: {halftone_img.size[0]}x{halftone_img.size[1]}")


# Batch processing utility
# ----------------------------------------------------------------------------

def batch_generate(input_dir: str, output_dir: str, count: int = 10):
    """
    Generate multiple variations for social media campaign.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    image_files = list(input_path.glob("*.jpg")) + list(input_path.glob("*.png"))
    
    styles = list(HALFTONE_STYLES.keys())
    colors = list(COLOR_SCHEMES.keys())
    
    for i in range(count):
        img_file = random.choice(image_files)
        style = random.choice(styles)
        color = random.choice(colors)
        quote = random.choice(MAMBA_QUOTES)
        
        output_file = output_path / f"mamba_{i+1:03d}_{style}_{color}.png"
        
        print(f"\n[{i+1}/{count}] Generating: {output_file.name}")
        
        # Process
        style_config = HALFTONE_STYLES[style]
        color_scheme = COLOR_SCHEMES[color]
        
        brightness_map = preprocess_image(
            str(img_file),
            TARGET_WIDTH,
            TARGET_HEIGHT,
            style_config["gamma"]
        )
        
        halftone_img = generate_classic_halftone(
            brightness_map,
            style_config,
            color_scheme["background"],
            color_scheme["dots"]
        )
        
        halftone_img = add_quote_overlay(
            halftone_img,
            quote,
            color_scheme,
            QUOTE_CONFIG
        )
        
        halftone_img.save(output_file, quality=95, dpi=(300, 300))
    
    print(f"\n✓ Generated {count} images in {output_dir}")


if __name__ == "__main__":
    main()


# ============================================================================
# USAGE EXAMPLES
# ============================================================================
"""
# Single image with classic black & white + red quote
python main.py --input portrait.jpg --output mamba_001.png --style classic_dots --color classic

# Lakers gold theme
python main.py --input portrait.jpg --output mamba_gold.png --style fine_dots --color lakers_gold

# Fingerprint/contour effect with copper tones
python main.py --input portrait.jpg --output mamba_copper.png --line-effect --color copper

# Custom quote
python main.py --input portrait.jpg --quote "I'M A FREQUENCY" --color mamba_red

# No quote overlay (pure halftone)
python main.py --input portrait.jpg --no-quote --color inverted

# Batch generate 20 variations
python main.py --batch --input-dir ./portraits --output-dir ./campaign --count 20
"""
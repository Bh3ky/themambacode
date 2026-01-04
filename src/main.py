# src/main.py

"""
Main entry point for halftone generator.
Handles CLI arguments and orchestrates the generation process.
"""

import argparse
import random
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    HALFTONE_STYLES, 
    COLOR_SCHEMES, 
    QUOTE_CONFIG, 
    MAMBA_QUOTES,
    TARGET_WIDTH, 
    TARGET_HEIGHT
)
from core.pre_processing import preprocess_image
from core.half_tone import (
    generate_classic_halftone,
    generate_line_halftone,
    generate_square_halftone
)
from core.quote_overlay import add_quote_overlay


def main():
    """Main CLI interface."""
    
    parser = argparse.ArgumentParser(
        description="Halftone Art Generator - Create stunning dot-based portrait art",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic usage with defaults
    python main.py --input portrait.jpg
    
    # Custom style and colors
    python main.py --input photo.jpg --style fine_dots --color lakers_gold
    
    # Line halftone effect
    python main.py --input photo.jpg --line-effect --color copper
    
    # Square dots instead of circles
    python main.py --input photo.jpg --square-effect
    
    # Without quote overlay
    python main.py --input photo.jpg --no-quote
    
    # Custom quote
    python main.py --input photo.jpg --quote "YOUR CUSTOM QUOTE HERE"
    
    # Batch generate variations
    python main.py --batch --input-dir ./photos --output-dir ./output --count 20
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--input", 
        help="Path to input image file"
    )
    
    # Optional arguments
    parser.add_argument(
        "--output", 
        default="output/halftone.png",
        help="Output file path (default: output/halftone.png)"
    )
    
    parser.add_argument(
        "--style",
        default="classic_dots",
        choices=list(HALFTONE_STYLES.keys()),
        help="Halftone style preset (default: classic_dots)"
    )
    
    parser.add_argument(
        "--color",
        default="classic",
        choices=list(COLOR_SCHEMES.keys()),
        help="Color scheme (default: classic)"
    )
    
    parser.add_argument(
        "--quote",
        default="random",
        help="Quote text or 'random' for random selection (default: random)"
    )
    
    parser.add_argument(
        "--no-quote",
        action="store_true",
        help="Generate without quote overlay"
    )
    
    # Effect type arguments
    effect_group = parser.add_mutually_exclusive_group()
    effect_group.add_argument(
        "--line-effect",
        action="store_true",
        help="Use contour line effect instead of dots"
    )
    effect_group.add_argument(
        "--square-effect",
        action="store_true",
        help="Use square dots instead of circles"
    )
    
    # Batch processing
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Enable batch processing mode"
    )
    parser.add_argument(
        "--input-dir",
        help="Input directory for batch processing"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory for batch processing (default: output)"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of variations to generate in batch mode (default: 10)"
    )
    
    # Advanced options
    parser.add_argument(
        "--cell-size",
        type=int,
        help="Override cell size (grid spacing)"
    )
    parser.add_argument(
        "--max-radius",
        type=float,
        help="Override maximum dot radius"
    )
    parser.add_argument(
        "--gamma",
        type=float,
        help="Override gamma correction value"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.batch:
        if not args.input_dir:
            parser.error("--batch requires --input-dir")
        batch_generate(args.input_dir, args.output_dir, args.count)
        return
    
    if not args.input:
        parser.error("--input is required (unless using --batch)")
    
    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load configurations
    style_config = HALFTONE_STYLES[args.style].copy()
    color_scheme = COLOR_SCHEMES[args.color]
    
    # Apply overrides if provided
    if args.cell_size:
        style_config["cell_size"] = args.cell_size
    if args.max_radius:
        style_config["max_radius"] = args.max_radius
    if args.gamma:
        style_config["gamma"] = args.gamma
    
    # Print processing info
    print("=" * 70)
    print("HALFTONE ART GENERATOR")
    print("=" * 70)
    print(f"Input:       {args.input}")
    print(f"Output:      {args.output}")
    print(f"Style:       {args.style}")
    print(f"Color:       {args.color}")
    print(f"Cell size:   {style_config['cell_size']}px")
    print(f"Max radius:  {style_config['max_radius']}px")
    print(f"Gamma:       {style_config['gamma']}")
    
    if args.line_effect:
        print(f"Effect:      Line/Contour")
    elif args.square_effect:
        print(f"Effect:      Square dots")
    else:
        print(f"Effect:      Classic circular dots")
    
    print("=" * 70)
    
    # Step 1: Preprocess image
    print("\n[1/3] Preprocessing image...")
    try:
        brightness_map = preprocess_image(
            args.input,
            TARGET_WIDTH,
            TARGET_HEIGHT,
            gamma=style_config["gamma"],
            enhanced_contrast=style_config.get("enhance_contrast", False)
        )
        print(f"      ✓ Processed to {TARGET_WIDTH}x{TARGET_HEIGHT}")
        print(f"      ✓ Brightness range: [{brightness_map.min():.2f}, {brightness_map.max():.2f}]")
    except Exception as e:
        print(f"      ✗ Error: {e}")
        return 1
    
    # Step 2: Generate halftone
    print("\n[2/3] Generating halftone...")
    try:
        if args.line_effect:
            halftone_img = generate_line_halftone(
                brightness_map,
                style_config,
                color_scheme["background"],
                color_scheme["dots"]
            )
            print(f"      ✓ Generated contour line halftone")
        elif args.square_effect:
            halftone_img = generate_square_halftone(
                brightness_map,
                style_config,
                color_scheme["background"],
                color_scheme["dots"]
            )
            print(f"      ✓ Generated square dot halftone")
        else:
            halftone_img = generate_classic_halftone(
                brightness_map,
                style_config,
                color_scheme["background"],
                color_scheme["dots"]
            )
            print(f"      ✓ Generated classic circular dot halftone")
    except Exception as e:
        print(f"      ✗ Error: {e}")
        return 1
    
    # Step 3: Add quote overlay (if requested)
    if not args.no_quote:
        print("\n[3/3] Adding quote overlay...")
        try:
            if args.quote == "random":
                quote = random.choice(MAMBA_QUOTES)
            else:
                quote = args.quote.upper()
            
            print(f"      Quote: {quote[:60]}{'...' if len(quote) > 60 else ''}")
            
            halftone_img = add_quote_overlay(
                halftone_img,
                quote,
                color_scheme,
                QUOTE_CONFIG
            )
            print(f"      ✓ Quote overlay added")
        except Exception as e:
            print(f"      ✗ Error: {e}")
            return 1
    else:
        print("\n[3/3] Skipping quote overlay (--no-quote)")
    
    # Save output
    print(f"\n[SAVE] Writing to {args.output}...")
    try:
        halftone_img.save(args.output, quality=95, dpi=(300, 300))
        file_size = Path(args.output).stat().st_size / (1024 * 1024)  # MB
        print(f"       ✓ Saved successfully ({file_size:.2f} MB)")
        print(f"       ✓ Dimensions: {halftone_img.size[0]}x{halftone_img.size[1]}")
    except Exception as e:
        print(f"       ✗ Error: {e}")
        return 1
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)
    return 0


def batch_generate(input_dir: str, output_dir: str, count: int = 10):
    """
    Generate multiple variations for social media campaigns.
    
    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save outputs
        count: Number of variations to generate
    """
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(ext))
    
    if not image_files:
        print(f"Error: No image files found in {input_dir}")
        return 1
    
    print("=" * 70)
    print("BATCH HALFTONE GENERATION")
    print("=" * 70)
    print(f"Input dir:   {input_dir}")
    print(f"Output dir:  {output_dir}")
    print(f"Images found: {len(image_files)}")
    print(f"Variations:  {count}")
    print("=" * 70)
    
    styles = list(HALFTONE_STYLES.keys())
    colors = list(COLOR_SCHEMES.keys())
    
    successful = 0
    failed = 0
    
    for i in range(count):
        # Randomly select parameters
        img_file = random.choice(image_files)
        style = random.choice(styles)
        color = random.choice(colors)
        quote = random.choice(MAMBA_QUOTES)
        
        # Generate output filename
        output_file = output_path / f"halftone_{i+1:03d}_{style}_{color}.png"
        
        print(f"\n[{i+1}/{count}] Generating: {output_file.name}")
        print(f"         Source: {img_file.name}")
        print(f"         Style:  {style}")
        print(f"         Color:  {color}")
        
        try:
            # Process
            style_config = HALFTONE_STYLES[style]
            color_scheme = COLOR_SCHEMES[color]
            
            brightness_map = preprocess_image(
                str(img_file),
                TARGET_WIDTH,
                TARGET_HEIGHT,
                gamma=style_config["gamma"],
                enhanced_contrast=style_config.get("enhance_contrast", False)
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
            print(f"         ✓ Success")
            successful += 1
            
        except Exception as e:
            print(f"         ✗ Failed: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print("BATCH GENERATION COMPLETE")
    print("=" * 70)
    print(f"Successful: {successful}/{count}")
    print(f"Failed:     {failed}/{count}")
    print(f"Output:     {output_dir}")
    print("=" * 70)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())


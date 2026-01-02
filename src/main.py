# src/main.py

import argparse
from core.pre_processing import preprocess_image
from core.half_tone import generate_dot_halftone

def main():
    parser = argparse.ArgumentParser(description="Mamba Mentality Halftone Generator")
    parser.add_argument("--input", required=True, help="Path to input image")
    parser.add_argument("--output", default="output/halftone.png", help="Output file")

    args = parser.parse_args()

    brightness_map = preprocess_image(args.input)
    halftone_img = generate_dot_halftone(brightness_map)
    halftone_img.save(args.output)

    print(f"Halftone image saved to {args.output}")

if __name__ == "__main__":
    main()
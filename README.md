## The Mamba Code: Mamba Mentality Halftone Art Generator

A Python tool that generates high-quality halftone portrait art combined with **Kobe Bryant-inspired "Mamba Mentality" quotes**, designed to program the mind for discipline, consistency, and excellence.

This project is built as a **coding challenge inspired by the Mamba mindset** - showing up daily, refining craft, and doing the work long after motivation fades. 

_DedicationOverTalent_ 🐍


## Philosophy

- High-quality halftone portrait generation
- Multiple halftone styles:
  - Dot-based
  - Radial
  - Fingerprint / flow-field (experimental)
- Minimalist quote overlays inspired by the Mamba Mentality
- High-resolution exports for social media
- Batch generation for daily content creation
- Clean, modular, production-grade Python codebase

## Project Structure

```text
src/
  core/        # Image processing & halftone algorithms
  utils/       # Helpers and utilities
  main.py      # Entry point
assets/        # Fonts and sample images
output/        # Generated content (ignored by git)
nbs/           # Experimenting with libraries
```

## Setup

```bash
git clone <repo-url>
cd halftone-art-generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py \
  --input assets/samples/portrait.jpg \
  --quote "Rest at the end, not in the middle." \
  --style radial
```

Quotes can be:
- Manually passed via CLI
- Pulled from a curated Mamba-inspired quote set
- Rotated daily for consistency-driven content

## Output

Generated images are saved to:
```text
output/

```

Note: Outputs are optimized for:
- Instagram
- X (Twitter)
- LinkedIn
- High-resolution poster formats

## Cdoing Challenge Aspect

This project is also a personal coding challenge, inspired by:
- Showing up daily
- Writing clean, maintainable code
- Improving systems incrementally
- Finishing what you start

The goal is not speed — it’s **craftsmanship**.


## License

MIT




### Qoute

> “The most important thing is to try and inspire people so that they can be great in whatever they want to do.” — Kobe Bryant

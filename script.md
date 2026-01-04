# Install dependencies
`pip install opencv-python pillow numpy`

# Generate single image
`python main.py --input kobe.jpg --output mamba_001.png`

# Lakers gold theme
`python main.py --input portrait.jpg --style fine_dots --color lakers_gold`

# Fingerprint effect with copper
`python main.py --input portrait.jpg --line-effect --color copper`

# Custom quote
python main.py --input photo.jpg --quote "DEDICATION MAKES DREAMS COME TRUE"


## 📱 **Social Media Optimized**
The 4:5 aspect ratio (2160x2700) is perfect for:
- Instagram posts
- Twitter/X
- Facebook
- Threads
- TikTok
- Reddit

## 🎨 **Next Steps to Complete**

You'll need to organize your code into this structure:
```
mamba-mentality-generator/
├── src/
│   ├── main.py
│   ├── config.py
│   └── core/
│       ├── preprocessing.py
│       ├── halftone.py
│       └── quote_overlay.py
├── input/
│   └── (your portrait images)
├── output/
│   └── (generated artwork)
└── requirements.txt


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


## Usage Examples

# Classic black & white with red quote
python src/main.py --input portrait.jpg --output art.png

# Lakers-themed with custom quote
python src/main.py --input kobe.jpg \
  --style classic_dots \
  --color lakers_gold \
  --quote "MAMBA MENTALITY"

# Fine detail newspaper style
python src/main.py --input photo.jpg \
  --style newspaper \
  --color inverted

# Generate 20 random variations
python src/main.py --batch \
  --input-dir ./photos \
  --output-dir ./campaign \
  --count 20


# Override default parameters
python src/main.py --input photo.jpg \
  --cell-size 10 \
  --max-radius 8 \
  --gamma 1.3

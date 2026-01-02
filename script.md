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
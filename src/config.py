# src/config.py

"""
Configuration for halftone generator.
All adjustable parameters in one place.
"""

# Image dimensions
TARGET_WIDTH = 2160   # 4K width for high quality
TARGET_HEIGHT = 2700  # Portrait aspect ratio (4:5 for Instagram)

# Color schemes
COLOR_SCHEMES = {
    "classic": {
        "background": (0, 0, 0),           # Black
        "dots": (255, 255, 255),           # White
        "quote_bg": (200, 0, 0),           # Red
        "quote_text": (255, 255, 255)      # White
    },
    "lakers_gold": {
        "background": (20, 20, 25),        # Near black
        "dots": (253, 185, 39),            # Lakers gold
        "quote_bg": (85, 37, 130),         # Lakers purple
        "quote_text": (253, 185, 39)       # Gold text
    },
    "copper": {
        "background": (15, 20, 25),        # Dark gray
        "dots": (184, 115, 51),            # Copper
        "quote_bg": (50, 30, 20),          # Dark brown
        "quote_text": (184, 115, 51)       # Copper text
    },
    "mamba_red": {
        "background": (0, 0, 0),           # Black
        "dots": (255, 255, 255),           # White
        "quote_bg": (200, 0, 0),           # Red
        "quote_text": (0, 0, 0)            # Black text
    },
    "inverted": {
        "background": (255, 255, 255),     # White
        "dots": (0, 0, 0),                 # Black
        "quote_bg": (0, 0, 0),             # Black
        "quote_text": (255, 255, 255)      # White text
    },
    "blue_steel": {
        "background": (10, 15, 25),        # Dark blue
        "dots": (180, 200, 220),           # Light blue
        "quote_bg": (30, 60, 100),         # Medium blue
        "quote_text": (220, 230, 240)      # Very light blue
    }
}

# Halftone styles
HALFTONE_STYLES = {
    "classic_dots": {
        "cell_size": 12,
        "max_radius": 7,
        "gamma": 1.2,          # Slight contrast boost
        "enhance_contrast": False
    },
    "fine_dots": {
        "cell_size": 8,
        "max_radius": 5,
        "gamma": 1.1,          # Minimal gamma for detail
        "enhance_contrast": False
    },
    "bold_dots": {
        "cell_size": 16,
        "max_radius": 10,
        "gamma": 1.3,          # More contrast for bold effect
        "enhance_contrast": False
    },
    "newspaper": {
        "cell_size": 10,
        "max_radius": 6,
        "gamma": 1.4,          # Higher gamma for softer look
        "enhance_contrast": False
    },
    "ultra_fine": {
        "cell_size": 6,
        "max_radius": 4,
        "gamma": 1.0,          # Linear for maximum detail
        "enhance_contrast": False
    },
    "artistic": {
        "cell_size": 14,
        "max_radius": 9,
        "gamma": 1.25,
        "enhance_contrast": True  # Use CLAHE for artistic effect
    }
}

# Quote overlay configuration
QUOTE_CONFIG = {
    "position": "top",      # 'top', 'bottom', or 'center'
    "padding": 40,          # Padding around text
    "font_size": 64,        # Font size in points
    "repeat_count": 12,     # Number of times to repeat quote
    "line_spacing": 8,      # Spacing between text lines
    "opacity": 1.0          # Banner opacity (0.0 to 1.0)
}

# Mamba Mentality quotes
MAMBA_QUOTES = [
    "HARD WORK OUTWEIGHS TALENT - EVERY TIME",
    "THE MOST IMPORTANT THING IS TO TRY AND INSPIRE PEOPLE",
    "MAMBA MENTALITY IS ABOUT OBSESSION",
    "EVERYTHING NEGATIVE IS AN OPPORTUNITY TO RISE",
    "THE MOMENT YOU GIVE UP IS THE MOMENT YOU LET SOMEONE ELSE WIN",
    "DEDICATION MAKES DREAMS COME TRUE",
    "I DON'T WANT TO BE THE NEXT MICHAEL JORDAN, I ONLY WANT TO BE KOBE BRYANT",
    "ONCE YOU KNOW WHAT FAILURE FEELS LIKE, DETERMINATION CHASES SUCCESS",
    "IF YOU'RE AFRAID TO FAIL, YOU DON'T DESERVE TO BE SUCCESSFUL",
    "THE MOST IMPORTANT THING IS YOU MUST PUT EVERYBODY ON NOTICE",
    "I CREATE MY OWN PATH",
    "BE WILLING TO SACRIFICE ANYTHING, BUT COMPROMISE NOTHING",
    "PAIN DOESN'T TELL YOU WHEN YOU OUGHT TO STOP",
    "I FOCUS ON ONE THING AND ONE THING ONLY - THAT'S TRYING TO WIN",
    "THERE'S NOTHING TRULY TO BE AFRAID OF, WHEN YOU THINK ABOUT IT",
    "I'LL DO WHATEVER IT TAKES TO WIN GAMES",
    "THE MINDSET ISN'T ABOUT SEEKING A RESULT",
    "I CREATE MY OWN REALITY",
    "FRIENDS CAN COME AND GO, BUT BANNERS HANG FOREVER",
    "I'M REFLECTIVE ONLY IN THE SENSE THAT I LEARN TO MOVE FORWARD"
]



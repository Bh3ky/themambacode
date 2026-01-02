# src/config.py

# Image processing
TARGET_WIDTH = 2160  # high-res for social media (4k)
TARGET_HEIGHT = 2700 # portrait aspect ratio [4:5 for instagram]


# Color schemes
COLOR_SCHEMES = {
    "classic": {
        "background": (0, 0, 0),
        "dots": (255, 255, 255),
        "quote_bg": (200, 0, 0),
        "quote_text": (255, 255, 255)
    },
    "lakers_gold": {
        "background": (20, 20, 25),
        "dots": (253, 185, 39), # gold
        "quote_bg": (85, 37, 130), # purple
        "quote_text": (253, 185, 39)
    },
    "copper": {
        "background": (15, 20, 25),
        "dots": (184, 115, 51), # copper
        "quote_bg": (85, 37, 130), # purple
        "quote_text": (253, 185, 39)
    },
    "mamba_red": {
        "background": (0, 0, 0),
        "dots": (255, 255, 255),
        "quote_bg": (200, 0, 0), 
        "quote_text": (0, 0, 0)
    },
    "inverted": {
        "background": (255, 255, 255),
        "dots": (0, 0, 0),
        "quote_bg": (0, 0, 0),
        "quote_text": (255, 255, 255)
    }
}

# halftone parameters
HALFTONE_STYLES = {
    "classic_dots": {
        "cell_size": 12,
        "max_radius": 7,
        "brightness_threshold": 0.85,  # Balanced threshold
        "gamma": 1.4  # Standard gamma for good contrast
    },
    "fine_dots": {
        "cell_size": 8,
        "max_radius": 5,
        "brightness_threshold": 0.82,  # Slightly lower for more detail
        "gamma": 1.6  # Higher gamma for finer detail
    },
    "bold_dots": {
        "cell_size": 16,
        "max_radius": 10,
        "brightness_threshold": 0.80,  # Lower threshold for bolder effect
        "gamma": 1.3  # Moderate gamma
    },
    "newspaper": {
        "cell_size": 10,
        "max_radius": 6,
        "brightness_threshold": 0.88,  # Higher threshold for newspaper look
        "gamma": 1.8  # Higher gamma for softer newspaper style
    }
}

# quote styling
QUOTE_CONFIG = {
    "position": "top",
    "padding": 40,  # Reduced padding for more compact banner
    "font_size": 64,  # Slightly smaller for better integration
    "repeat_count": 12,  # More repetitions for continuous text effect
    "line_spacing": 8,
    "opacity": 1.0  # Full opacity for solid banner
}

# Sample Kobe Bryant "Mamba Mentality" Quotes
MAMBA_QUOTES = [
    "THE MOST IMPORTANT THING IS TO TRY AND INSPIRE PEOPLE",
    "I'M A FREQUENCY",
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
    "HARD WORK OUTWEIGHS TALENT - EVERY TIME",
    "I'LL DO WHATEVER IT TAKES TO WIN GAMES",
    "THE MINDSET ISN'T ABOUT SEEKING A RESULT",
    "I CREATE MY OWN REALITY",
    "FRIENDS CAN COME AND GO, BUT BANNERS HANG FOREVER"
]


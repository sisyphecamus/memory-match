# Memory Match v2.0 — Theme and difficulty definitions

THEMES = {
    "Vaporwave": {
        "name": "Vaporwave",
        "mode": "dark",
        "bg": "#1A0A2E",
        "text": "#E8D5F5",
        "accent": "#FF6B9D",
        "card_colors": {
            "back_base": "#2D1B4E",
            "back_border": "#00D4FF",
            "back_pattern": "#B44DFF",
            "face_base": "#1E1035",
            "face_border": "#00D4FF",
            "symbol": "#FF6B9D",
        },
        "pattern": "vaporwave",
    },
    "Cyberpunk": {
        "name": "Cyberpunk",
        "mode": "dark",
        "bg": "#0A0A14",
        "text": "#C8D6E5",
        "accent": "#00D4FF",
        "card_colors": {
            "back_base": "#1A1A1E",
            "back_border": "#00D4FF",
            "back_pattern": "#00D4FF",
            "face_base": "#151530",
            "face_border": "#00D4FF",
            "symbol": "#00D4FF",
        },
        "pattern": "hex_chip",
    },
    "Nature": {
        "name": "Nature",
        "mode": "dark",
        "bg": "#17261B",
        "text": "#D4EDDA",
        "accent": "#F59E0B",
        "card_colors": {
            "back_base": "#1A3A2A",
            "back_border": "#059669",
            "back_pattern": "#34D399",
            "face_base": "#F0FAF2",
            "face_border": "#15803D",
            "symbol": "#059669",
        },
        "pattern": "tree_of_life",
    },
}

DIFFICULTIES = {
    "Easy (4×4)": (4, 4),
    "Medium (4×6)": (4, 6),
    "Hard (6×6)": (6, 6),
}

_ROMAN = [
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def to_roman(n):
    """Convert an integer to Roman numerals."""
    result = ""
    for value, numeral in _ROMAN:
        while n >= value:
            result += numeral
            n -= value
    return result

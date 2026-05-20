from .nature import NATURE_SYMBOLS, draw_nature
from .cyberpunk import CYBERPUNK_SYMBOLS, draw_cyberpunk
from .vaporwave import VAPORWAVE_SYMBOLS, draw_vaporwave


def draw_symbol(draw, cx, cy, s, name, color, theme):
    """Dispatch a symbol draw to the correct theme drawer."""
    if theme == "Cyberpunk":
        return draw_cyberpunk(draw, cx, cy, s, name, color)
    elif theme == "Vaporwave":
        return draw_vaporwave(draw, cx, cy, s, name, color)
    else:
        return draw_nature(draw, cx, cy, s, name, color)

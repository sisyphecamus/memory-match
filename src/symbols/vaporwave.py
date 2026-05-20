"""Vaporwave-themed illustration functions for Memory Match cards."""

import math
from PIL import Image, ImageDraw, ImageFont

VAPORWAVE_SYMBOLS = [
    "statue", "palm_tree", "dolphin", "floppy_disk",
    "sunset_circle", "grid_floor", "mountain", "crystal",
    "cassette", "neon_triangle", "cherry_blossom", "synthwave",
    "lightning", "crt_monitor", "yinyang", "retro_phone",
    "diamond", "star",
]

_FONT_PATH = "/Users/lemon/.claude/skills/canvas-design/canvas-fonts"


def draw_vaporwave(draw, cx, cy, s, name, color):
    drawer = _DRAWERS.get(name)
    if drawer:
        drawer(draw, cx, cy, s, color)
    else:
        draw.ellipse([cx - s * 0.5, cy - s * 0.5, cx + s * 0.5, cy + s * 0.5], fill=color)


def _draw_statue(draw, cx, cy, s, color):
    """Greek statue bust with sunglasses."""
    # Head
    draw.ellipse([cx - s * 0.3, cy - s * 0.55, cx + s * 0.3, cy - s * 0.05], fill=color)
    # Neck
    draw.rectangle([cx - s * 0.08, cy - s * 0.05, cx + s * 0.08, cy + s * 0.15], fill=color)
    # Shoulders
    draw.ellipse([cx - s * 0.55, cy + s * 0.05, cx + s * 0.55, cy + s * 0.4], fill=color)
    # Sunglasses
    for side in [-1, 1]:
        sg_x1 = cx + side * s * 0.18
        sg_x2 = cx + side * s * 0.04
        if sg_x1 > sg_x2:
            sg_x1, sg_x2 = sg_x2, sg_x1
        draw.rectangle([sg_x1, cy - s * 0.35, sg_x2, cy - s * 0.15], fill=(0, 0, 0, 200))
    draw.rectangle([cx - s * 0.04, cy - s * 0.35, cx + s * 0.04, cy - s * 0.15], fill=(0, 0, 0, 200))


def _draw_palm_tree(draw, cx, cy, s, color):
    """Palm tree silhouette."""
    # Trunk
    for i in range(8):
        y = cy + s * 0.2 + i * s * 0.07
        off = math.sin(i * 0.8) * s * 0.06
        draw.line([(cx + off, y), (cx + off, y + s * 0.07)], fill=color, width=max(2, int(s * 0.04)))
    # Fronds
    for a_idx in range(7):
        angle = math.radians(-110 + a_idx * 35)
        length = s * 0.6 if a_idx in [2, 3, 4] else s * 0.4
        ex = cx + length * math.cos(angle)
        ey = cy + s * 0.1 + length * math.sin(angle)
        draw.line([(cx, cy + s * 0.15), (ex, ey)], fill=color, width=2)
        # Leaflets
        for frac in [0.4, 0.7]:
            lx = cx + frac * (ex - cx)
            ly = cy + s * 0.15 + frac * (ey - (cy + s * 0.15))
            for side in [-1, 1]:
                slx = lx + side * s * 0.08 * math.sin(angle + 1.5)
                sly = ly + side * s * 0.08 * math.cos(angle + 1.5)
                draw.line([(lx, ly), (slx, sly)], fill=color, width=1)


def _draw_dolphin(draw, cx, cy, s, color):
    """Low-poly dolphin silhouette."""
    pts = [
        (cx - s * 0.15, cy + s * 0.45), (cx - s * 0.5, cy + s * 0.15),
        (cx - s * 0.55, cy - s * 0.1), (cx - s * 0.3, cy - s * 0.3),
        (cx - s * 0.1, cy - s * 0.4), (cx + s * 0.15, cy - s * 0.35),
        (cx + s * 0.35, cy - s * 0.15), (cx + s * 0.5, cy + s * 0.1),
        (cx + s * 0.3, cy + s * 0.2), (cx + s * 0.1, cy + s * 0.35),
        (cx - s * 0.05, cy + s * 0.5),
    ]
    draw.polygon(pts, fill=color)
    # Eye
    draw.ellipse([cx + s * 0.1, cy - s * 0.2, cx + s * 0.2, cy - s * 0.1], fill=(0, 0, 0, 120))


def _draw_floppy_disk(draw, cx, cy, s, color):
    """Floppy disk icon."""
    draw.rectangle([cx - s * 0.45, cy - s * 0.55, cx + s * 0.45, cy + s * 0.55], fill=color)
    # Metal slider area
    draw.rectangle([cx + s * 0.15, cy - s * 0.55, cx + s * 0.45, cy - s * 0.15], fill=(0, 0, 0, 80))
    # Label area
    draw.rectangle([cx - s * 0.3, cy - s * 0.15, cx + s * 0.3, cy + s * 0.35], fill=(0, 0, 0, 40))
    # Lines on label
    for i in range(3):
        ly = cy + i * s * 0.12
        draw.line([(cx - s * 0.2, ly), (cx + s * 0.2, ly)], fill=(0, 0, 0, 80), width=1)


def _draw_sunset_circle(draw, cx, cy, s, color):
    """Split circle — half sun half dark with grid line."""
    draw.ellipse([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55], fill=color)
    # Horizon line
    draw.line([(cx - s * 0.6, cy + s * 0.05), (cx + s * 0.6, cy + s * 0.05)], fill=(0, 0, 0, 80), width=2)
    # Lower half darker
    draw.ellipse([cx - s * 0.55, cy + s * 0.05, cx + s * 0.55, cy + s * 0.55], fill=(0, 0, 0, 40))


def _draw_grid_floor(draw, cx, cy, s, color):
    """Perspective grid floor."""
    # Horizon
    draw.line([(cx - s * 0.5, cy - s * 0.25), (cx + s * 0.5, cy - s * 0.25)], fill=color, width=1)
    # Perspective lines
    for i in range(-3, 4):
        bx = cx + i * s * 0.12
        draw.line([(cx, cy - s * 0.25), (bx, cy + s * 0.5)], fill=color, width=1)
    # Horizontal grid lines
    for i in range(5):
        frac = 0.3 + i * 0.15
        y = cy - s * 0.25 + frac * s * 0.8
        spread = frac * s * 0.45
        draw.line([(cx - spread, y), (cx + spread, y)], fill=color, width=1)


def _draw_mountain(draw, cx, cy, s, color):
    """Geometric low-poly mountain."""
    # Main peak
    draw.polygon([(cx - s * 0.5, cy + s * 0.4), (cx, cy - s * 0.55), (cx + s * 0.5, cy + s * 0.4)], fill=color)
    # Left side shadow
    draw.polygon([(cx - s * 0.5, cy + s * 0.4), (cx, cy - s * 0.55), (cx, cy + s * 0.4)], fill=(0, 0, 0, 50))
    # Snow cap
    draw.polygon([(cx - s * 0.12, cy - s * 0.2), (cx, cy - s * 0.55), (cx + s * 0.08, cy - s * 0.18)], fill=(255, 255, 255, 120))
    # Secondary peak
    draw.polygon([(cx + s * 0.2, cy + s * 0.4), (cx + s * 0.55, cy - s * 0.1), (cx + s * 0.7, cy + s * 0.4)], fill=color)


def _draw_crystal(draw, cx, cy, s, color):
    """Faceted crystal/gem."""
    # Hexagonal crystal
    pts = [
        (cx, cy - s * 0.6),
        (cx + s * 0.25, cy - s * 0.2),
        (cx + s * 0.3, cy + s * 0.4),
        (cx, cy + s * 0.55),
        (cx - s * 0.3, cy + s * 0.4),
        (cx - s * 0.25, cy - s * 0.2),
    ]
    draw.polygon(pts, fill=color)
    # Facet lines
    draw.line([(cx, cy - s * 0.55), (cx, cy + s * 0.55)], fill=(0, 0, 0, 60), width=1)
    draw.line([(cx - s * 0.15, cy + s * 0.05), (cx + s * 0.15, cy - s * 0.1)], fill=(0, 0, 0, 40), width=1)
    # Highlight
    draw.polygon([(cx - s * 0.12, cy - s * 0.15), (cx - s * 0.05, cy + s * 0.1), (cx + s * 0.15, cy + s * 0.05)], fill=(255, 255, 255, 60))


def _draw_cassette(draw, cx, cy, s, color):
    """Cassette tape."""
    draw.rounded_rectangle([cx - s * 0.5, cy - s * 0.35, cx + s * 0.5, cy + s * 0.5], radius=int(s * 0.08), fill=color)
    # Label area
    draw.rectangle([cx - s * 0.3, cy - s * 0.15, cx + s * 0.3, cy + s * 0.2], fill=(0, 0, 0, 50))
    # Reels
    for side in [-1, 1]:
        draw.ellipse([cx + side * s * 0.2 - s * 0.1, cy - s * 0.05 - s * 0.1,
                      cx + side * s * 0.2 + s * 0.1, cy - s * 0.05 + s * 0.1], fill=(0, 0, 0, 100))
        draw.ellipse([cx + side * s * 0.2 - s * 0.03, cy - s * 0.05 - s * 0.03,
                      cx + side * s * 0.2 + s * 0.03, cy - s * 0.05 + s * 0.03], fill=(0, 0, 0, 60))


def _draw_neon_triangle(draw, cx, cy, s, color):
    """Neon triangle with glow lines."""
    pts = [(cx, cy - s * 0.6), (cx + s * 0.55, cy + s * 0.45), (cx - s * 0.55, cy + s * 0.45)]
    draw.polygon(pts, fill=None, outline=color, width=3)
    # Inner triangle
    inner = [(cx, cy - s * 0.3), (cx + s * 0.3, cy + s * 0.25), (cx - s * 0.3, cy + s * 0.25)]
    draw.polygon(inner, fill=None, outline=color, width=1)


def _draw_cherry_blossom(draw, cx, cy, s, color):
    """Cherry blossom — five petals with center."""
    for i in range(5):
        a = math.radians(i * 72 - 90)
        px = cx + s * 0.45 * math.cos(a)
        py = cy + s * 0.45 * math.sin(a)
        draw.ellipse([px - s * 0.22, py - s * 0.25, px + s * 0.22, py + s * 0.25], fill=color)
        # Petal crease
        draw.line([(cx, cy), (px, py)], fill=(255, 255, 255, 40), width=1)
    # Center
    draw.ellipse([cx - s * 0.08, cy - s * 0.08, cx + s * 0.08, cy + s * 0.08], fill=(255, 220, 200, 200))
    for _ in range(5):
        dx = (random.random() - 0.5) * s * 0.06
        dy = (random.random() - 0.5) * s * 0.06
        draw.ellipse([cx + dx - 1, cy + dy - 1, cx + dx + 1, cy + dy + 1], fill=color)


def _draw_synthwave(draw, cx, cy, s, color):
    """Synthwave sun with horizontal bands."""
    # Sun
    draw.ellipse([cx - s * 0.35, cy - s * 0.35, cx + s * 0.35, cy + s * 0.35], fill=color)
    # Horizontal bands (like retro sunset)
    stripes = [
        (cy - s * 0.6, cy - s * 0.45),
        (cy - s * 0.35, cy - s * 0.2),
        (cy - s * 0.1, cy + s * 0.05),
    ]
    for y1, y2 in stripes:
        draw.rectangle([cx - s * 0.55, y1, cx + s * 0.55, y2], fill=color)
    # Sun overlaps bands
    draw.ellipse([cx - s * 0.35, cy - s * 0.35, cx + s * 0.35, cy + s * 0.35], fill=None, outline=color, width=2)


def _draw_lightning(draw, cx, cy, s, color):
    """Sharp lightning bolt."""
    pts = [
        (cx + s * 0.05, cy - s * 0.6),
        (cx - s * 0.4, cy - s * 0.05),
        (cx - s * 0.05, cy - s * 0.05),
        (cx - s * 0.1, cy + s * 0.6),
        (cx + s * 0.3, cy + s * 0.05),
        (cx - s * 0.1, cy + s * 0.05),
    ]
    draw.polygon(pts, fill=color)


def _draw_crt_monitor(draw, cx, cy, s, color):
    """Retro CRT computer monitor."""
    # Screen bezel
    draw.rounded_rectangle([cx - s * 0.5, cy - s * 0.55, cx + s * 0.5, cy + s * 0.15], radius=int(s * 0.06), fill=color)
    # Screen
    draw.rectangle([cx - s * 0.38, cy - s * 0.43, cx + s * 0.38, cy + s * 0.03], fill=(0, 0, 0, 80))
    # Scan line
    draw.line([(cx - s * 0.35, cy - s * 0.2), (cx + s * 0.35, cy - s * 0.2)], fill=(255, 255, 255, 60), width=1)
    # Stand
    draw.rectangle([cx - s * 0.15, cy + s * 0.15, cx + s * 0.15, cy + s * 0.3], fill=color)
    draw.rectangle([cx - s * 0.25, cy + s * 0.3, cx + s * 0.25, cy + s * 0.4], fill=color)


def _draw_yinyang(draw, cx, cy, s, color):
    """Vaporwave yin-yang (split circle)."""
    # Main circle
    draw.ellipse([cx - s * 0.5, cy - s * 0.5, cx + s * 0.5, cy + s * 0.5], fill=None, outline=color, width=2)
    # Top half filled
    draw.pieslice([cx - s * 0.5, cy - s * 0.5, cx + s * 0.5, cy + s * 0.5], start=270, end=90, fill=color)
    # Dots
    draw.ellipse([cx - s * 0.12, cy - s * 0.3, cx + s * 0.12, cy - s * 0.05], fill=color)
    draw.ellipse([cx - s * 0.12, cy + s * 0.05, cx + s * 0.12, cy + s * 0.3], fill=(255, 255, 255, 120))


def _draw_retro_phone(draw, cx, cy, s, color):
    """Retro landline phone."""
    # Base
    draw.rounded_rectangle([cx - s * 0.35, cy - s * 0.05, cx + s * 0.35, cy + s * 0.45], radius=int(s * 0.1), fill=color)
    # Handset
    draw.rounded_rectangle([cx - s * 0.3, cy - s * 0.45, cx + s * 0.3, cy + s * 0.05], radius=int(s * 0.15), fill=None, outline=color, width=2)
    # Coiled cord
    for i in range(5):
        cy2 = cy + s * 0.45 + i * s * 0.06
        off = 3 * (-1 if i % 2 == 0 else 1)
        draw.line([(cx + off, cy2), (cx - off, cy2)], fill=color, width=1)


def _draw_diamond(draw, cx, cy, s, color):
    """Geometric diamond shape."""
    pts = [(cx, cy - s * 0.6), (cx + s * 0.5, cy), (cx, cy + s * 0.6), (cx - s * 0.5, cy)]
    draw.polygon(pts, fill=color)
    # Internal facets
    draw.line([(cx, cy - s * 0.55), (cx, cy + s * 0.55)], fill=(0, 0, 0, 50), width=1)
    draw.line([(cx - s * 0.25, cy - s * 0.1), (cx + s * 0.25, cy - s * 0.1)], fill=(0, 0, 0, 40), width=1)
    draw.line([(cx - s * 0.3, cy + s * 0.2), (cx + s * 0.3, cy + s * 0.2)], fill=(0, 0, 0, 40), width=1)
    # Sparkle
    draw.ellipse([cx - s * 0.06, cy - s * 0.45, cx + s * 0.06, cy - s * 0.33], fill=(255, 255, 255, 100))


def _draw_star(draw, cx, cy, s, color):
    """Five-pointed star."""
    pts = []
    for i in range(10):
        r = s * 0.55 if i % 2 == 0 else s * 0.25
        a = math.radians(i * 36 - 90)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=color)


import random

_DRAWERS = {
    "statue": _draw_statue, "palm_tree": _draw_palm_tree, "dolphin": _draw_dolphin,
    "floppy_disk": _draw_floppy_disk, "sunset_circle": _draw_sunset_circle,
    "grid_floor": _draw_grid_floor, "mountain": _draw_mountain, "crystal": _draw_crystal,
    "cassette": _draw_cassette, "neon_triangle": _draw_neon_triangle,
    "cherry_blossom": _draw_cherry_blossom, "synthwave": _draw_synthwave,
    "lightning": _draw_lightning, "crt_monitor": _draw_crt_monitor,
    "yinyang": _draw_yinyang, "retro_phone": _draw_retro_phone,
    "diamond": _draw_diamond, "star": _draw_star,
}

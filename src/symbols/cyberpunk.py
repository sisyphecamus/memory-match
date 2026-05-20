"""Cyberpunk-themed illustration functions for Memory Match cards."""

import math
from PIL import ImageFont

CYBERPUNK_SYMBOLS = [
    "credits", "data_chip", "energy_core", "hacking", "vector_blade",
    "firewall", "augment", "neural_ai", "toxin", "drone",
    "network_node", "encryption", "scanner", "exoskeleton", "nanoswarm",
    "cyberdeck", "glitch", "uplink",
]

_FONT_PATH = "/Users/lemon/.claude/skills/canvas-design/canvas-fonts/JetBrainsMono-Bold.ttf"


def draw_cyberpunk(draw, cx, cy, s, name, color):
    """Draw a cyberpunk illustration."""
    drawer = _DRAWERS.get(name)
    if drawer:
        drawer(draw, cx, cy, s, color)
    else:
        draw.ellipse([cx - s * 0.5, cy - s * 0.5, cx + s * 0.5, cy + s * 0.5], fill=color)


def _draw_credits(draw, cx, cy, s, color):
    pts = []
    for i in range(6):
        a = math.radians(i * 60 - 30)
        pts.append((cx + s * 0.7 * math.cos(a), cy + s * 0.7 * math.sin(a)))
    draw.polygon(pts, fill=None, outline=color, width=2)
    for off in [-s * 0.18, s * 0.18]:
        draw.line([(cx - s * 0.4, cy + off), (cx + s * 0.4, cy - off)], fill=color, width=2)


def _draw_data_chip(draw, cx, cy, s, color):
    draw.rounded_rectangle([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55],
                           radius=int(s * 0.1), fill=None, outline=color, width=2)
    draw.rectangle([cx + s * 0.25, cy - s * 0.55, cx + s * 0.55, cy - s * 0.25], fill=color)
    for col in [-2, 0, 2]:
        for row in [-2, -1, 0, 1, 2]:
            dx = col * s * 0.13
            dy = row * s * 0.13
            draw.ellipse([cx + dx - 1, cy + dy - 1, cx + dx + 1, cy + dy + 1], fill=color)


def _draw_energy_core(draw, cx, cy, s, color):
    for a in range(0, 360, 20):
        ar = math.radians(a)
        r = s * 0.65
        x1 = cx + r * math.cos(ar)
        y1 = cy + r * math.sin(ar)
        ar2 = math.radians(a + 10)
        x2 = cx + r * math.cos(ar2)
        y2 = cy + r * math.sin(ar2)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
    pts = [(cx - s * 0.05, cy - s * 0.55), (cx - s * 0.3, cy - s * 0.05),
           (cx + s * 0.05, cy - s * 0.05), (cx + s * 0.05, cy + s * 0.15),
           (cx + s * 0.3, cy - s * 0.2), (cx - s * 0.05, cy + s * 0.55)]
    for i in range(0, len(pts) - 1, 2):
        draw.line(pts[i:i + 2], fill=color, width=2)


def _draw_hacking(draw, cx, cy, s, color):
    try:
        font = ImageFont.truetype(_FONT_PATH, size=max(10, int(s * 0.5)))
        draw.text((cx - s * 0.25, cy - s * 0.4), ">_", fill=color, font=font)
    except Exception:
        draw.text((cx - s * 0.2, cy - s * 0.35), ">_", fill=color)
    pts = [(cx - s * 0.4, cy + s * 0.05), (cx, cy + s * 0.55), (cx + s * 0.4, cy + s * 0.05)]
    draw.polygon(pts, fill=None, outline=color, width=2)
    ch = cy + s * 0.25
    draw.line([(cx - s * 0.12, ch), (cx + s * 0.12, ch)], fill=color, width=1)
    draw.line([(cx, ch - s * 0.1), (cx, ch + s * 0.1)], fill=color, width=1)


def _draw_vector_blade(draw, cx, cy, s, color):
    pts = [(cx, cy - s * 0.7), (cx + s * 0.25, cy - s * 0.15),
           (cx + s * 0.05, cy - s * 0.1), (cx + s * 0.05, cy + s * 0.5),
           (cx - s * 0.05, cy + s * 0.5), (cx - s * 0.05, cy - s * 0.1),
           (cx - s * 0.25, cy - s * 0.15)]
    draw.polygon(pts, fill=color)


def _draw_firewall(draw, cx, cy, s, color):
    hex_size = s * 0.2
    pts = [(cx, cy - s * 0.65), (cx + s * 0.55, cy - s * 0.35),
           (cx + s * 0.55, cy + s * 0.15), (cx, cy + s * 0.6),
           (cx - s * 0.55, cy + s * 0.15), (cx - s * 0.55, cy - s * 0.35)]
    draw.polygon(pts, fill=None, outline=color, width=2)
    for grid_r in range(-1, 2):
        for grid_c in range(-1, 2):
            hx = cx + grid_c * hex_size * 1.8
            hy = cy + grid_r * hex_size * 1.7
            if abs(grid_c) <= 1 and abs(grid_r) <= 1 and not (grid_r == -1 and abs(grid_c) == 1):
                hpts = []
                for i in range(6):
                    a = math.radians(i * 60)
                    hpts.append((hx + hex_size * math.cos(a), hy + hex_size * math.sin(a)))
                fill_hex = color if (grid_r + grid_c) % 2 == 0 else None
                draw.polygon(hpts, fill=fill_hex, outline=color, width=1)


def _draw_augment(draw, cx, cy, s, color):
    draw.rectangle([cx - s * 0.06, cy + s * 0.15, cx + s * 0.06, cy + s * 0.65], fill=color)
    draw.rounded_rectangle([cx - s * 0.25, cy - s * 0.3, cx + s * 0.25, cy + s * 0.2],
                           radius=int(s * 0.12), fill=color)
    for fx in [-0.3, -0.1, 0.1, 0.3]:
        f_x = cx + fx * s * 0.6
        draw.rounded_rectangle([f_x - s * 0.06, cy - s * 0.65, f_x + s * 0.06, cy - s * 0.2],
                               radius=int(s * 0.06), fill=color)
    for ty in [cy + s * 0.3, cy + s * 0.4, cy + s * 0.5]:
        draw.line([(cx - s * 0.2, ty), (cx + s * 0.2, ty)], fill=(0, 0, 0, 100), width=1)
        for vx in [cx - s * 0.1, cx + s * 0.1]:
            draw.ellipse([vx - 1, ty - 1, vx + 1, ty + 1], fill=(0, 0, 0, 120))


def _draw_neural_ai(draw, cx, cy, s, color):
    outer = [(0, -0.3, 0.3, -0.3), (0.3, -0.3, 0.3, 0.3), (0.3, 0.3, 0, 0.3),
             (0, 0.3, -0.3, 0.3), (-0.3, 0.3, -0.3, -0.3), (-0.3, -0.3, 0, -0.3)]
    inner = [(0, -0.15, 0.15, -0.15), (0.15, -0.15, 0.15, 0.15), (0.15, 0.15, 0, 0.15),
             (0, 0.15, -0.15, 0.15), (-0.15, 0.15, -0.15, -0.15), (-0.15, -0.15, 0, -0.15)]
    for segments, w in [(outer, 2), (inner, 1)]:
        for x1f, y1f, x2f, y2f in segments:
            draw.line([(cx + x1f * s, cy + y1f * s), (cx + x2f * s, cy + y2f * s)], fill=color, width=w)


def _draw_toxin(draw, cx, cy, s, color):
    pts = [(cx, cy + s * 0.55), (cx + s * 0.55, cy - s * 0.45), (cx - s * 0.55, cy - s * 0.45)]
    draw.polygon(pts, fill=color)
    for i in range(3):
        sy = cy - s * 0.35 + i * s * 0.2
        sw = s * 0.45 * (1 - i * 0.25)
        draw.line([(cx - sw, sy), (cx + sw, sy)], fill=(0, 0, 0, 80), width=2)
    dot_r = s * 0.08
    draw.ellipse([cx - dot_r, cy - s * 0.05 - dot_r * 2, cx + dot_r, cy - s * 0.05], fill=(0, 0, 0, 80))


def _draw_drone(draw, cx, cy, s, color):
    for a in [45, 135, 225, 315]:
        ar = math.radians(a)
        draw.line([(cx, cy), (cx + s * 0.6 * math.cos(ar), cy + s * 0.6 * math.sin(ar))], fill=color, width=2)
        rx = cx + s * 0.6 * math.cos(ar)
        ry = cy + s * 0.6 * math.sin(ar)
        draw.ellipse([rx - s * 0.12, ry - s * 0.12, rx + s * 0.12, ry + s * 0.12], fill=None, outline=color, width=1)
    draw.ellipse([cx - s * 0.2, cy - s * 0.2, cx + s * 0.2, cy + s * 0.2], fill=color)
    draw.ellipse([cx - s * 0.05, cy - s * 0.05, cx + s * 0.05, cy + s * 0.05], fill=(0, 0, 0, 150))


def _draw_network_node(draw, cx, cy, s, color):
    nodes = [(cx - s * 0.4, cy - s * 0.4), (cx + s * 0.4, cy - s * 0.4), (cx, cy),
             (cx - s * 0.35, cy + s * 0.35), (cx + s * 0.35, cy + s * 0.35)]
    edges = [(0, 2), (1, 2), (2, 3), (2, 4), (0, 1), (3, 4)]
    for i, j in edges:
        draw.line([nodes[i], nodes[j]], fill=color, width=1)
    for nx, ny in nodes:
        draw.ellipse([nx - s * 0.1, ny - s * 0.1, nx + s * 0.1, ny + s * 0.1], fill=color)


def _draw_encryption(draw, cx, cy, s, color):
    draw.rectangle([cx - s * 0.3, cy + s * 0.05, cx + s * 0.3, cy + s * 0.5], fill=color)
    draw.arc([cx - s * 0.2, cy - s * 0.45, cx + s * 0.2, cy + s * 0.1], start=180, end=360, fill=None, width=2)
    draw.ellipse([cx - s * 0.06, cy + s * 0.15, cx + s * 0.06, cy + s * 0.25], fill=(0, 0, 0, 120))
    draw.rectangle([cx - s * 0.03, cy + s * 0.22, cx + s * 0.03, cy + s * 0.38], fill=(0, 0, 0, 120))


def _draw_scanner(draw, cx, cy, s, color):
    for r_frac in [0.25, 0.5, 0.7]:
        r = s * r_frac
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=None, outline=color, width=1)
    sweep = [(cx, cy), (cx + s * 0.65, cy - s * 0.3), (cx + s * 0.65, cy + s * 0.3)]
    draw.polygon(sweep, fill=color)
    draw.ellipse([cx - s * 0.05, cy - s * 0.05, cx + s * 0.05, cy + s * 0.05], fill=color)


def _draw_exoskeleton(draw, cx, cy, s, color):
    segments = 5
    seg_h = s * 0.85 / segments
    for i in range(segments):
        sy = cy - s * 0.4 + i * seg_h
        w = s * 0.35 if i % 2 == 0 else s * 0.25
        draw.rectangle([cx - w, sy, cx + w, sy + seg_h * 0.85], fill=color if i % 2 == 0 else None, outline=color, width=1)
        if i > 0:
            jy = sy
            draw.ellipse([cx - s * 0.06, jy - s * 0.04, cx + s * 0.06, jy + s * 0.04], fill=color)


def _draw_nanoswarm(draw, cx, cy, s, color):
    pos = [(cx - s * 0.3, cy - s * 0.3), (cx + s * 0.2, cy - s * 0.4), (cx, cy - s * 0.05),
           (cx - s * 0.35, cy + s * 0.2), (cx + s * 0.3, cy + s * 0.25),
           (cx - s * 0.1, cy + s * 0.5), (cx + s * 0.15, cy + s * 0.55), (cx + s * 0.4, cy - s * 0.05)]
    sizes = [s * 0.15, s * 0.12, s * 0.18, s * 0.1, s * 0.14, s * 0.08, s * 0.13, s * 0.11]
    for (px, py), sz in zip(pos, sizes):
        draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=color)


def _draw_cyberdeck(draw, cx, cy, s, color):
    draw.rounded_rectangle([cx - s * 0.6, cy - s * 0.3, cx + s * 0.6, cy + s * 0.55],
                           radius=int(s * 0.08), fill=None, outline=color, width=2)
    for row in range(4):
        ry = cy - s * 0.15 + row * s * 0.15
        keys_in_row = 5 - (row % 2)
        for k in range(keys_in_row):
            kx = cx + (k - (keys_in_row - 1) / 2) * s * 0.2
            kw, kh = s * 0.07, s * 0.04
            draw.rectangle([kx - kw, ry - kh, kx + kw, ry + kh], fill=color if row == 3 else None, outline=color, width=1)


def _draw_glitch(draw, cx, cy, s, color):
    draw.rectangle([cx - s * 0.45, cy - s * 0.5, cx - s * 0.05, cy - s * 0.1], fill=color)
    draw.rectangle([cx + s * 0.05, cy - s * 0.35, cx + s * 0.4, cy + s * 0.05], fill=color)
    draw.rectangle([cx - s * 0.3, cy + s * 0.15, cx + s * 0.1, cy + s * 0.5], fill=color)
    for lx in [cx - s * 0.1, cx + s * 0.15]:
        draw.line([(lx, cy - s * 0.55), (lx + s * 0.08, cy + s * 0.55)], fill=color, width=1)


def _draw_uplink(draw, cx, cy, s, color):
    draw.arc([cx - s * 0.6, cy - s * 0.4, cx + s * 0.6, cy + s * 0.6], start=20, end=160, fill=None, width=2)
    draw.line([(cx, cy), (cx - s * 0.2, cy + s * 0.25)], fill=color, width=1)
    draw.ellipse([cx - s * 0.05, cy - s * 0.05, cx + s * 0.05, cy + s * 0.05], fill=color)
    for i in range(3):
        r = s * (0.12 + i * 0.1)
        draw.arc([cx - r, cy - s * 0.85 + i * s * 0.08, cx + r, cy - s * 0.5 + r], start=300, end=200, fill=None, width=1)


_DRAWERS = {
    "credits": _draw_credits, "data_chip": _draw_data_chip, "energy_core": _draw_energy_core,
    "hacking": _draw_hacking, "vector_blade": _draw_vector_blade, "firewall": _draw_firewall,
    "augment": _draw_augment, "neural_ai": _draw_neural_ai, "toxin": _draw_toxin,
    "drone": _draw_drone, "network_node": _draw_network_node, "encryption": _draw_encryption,
    "scanner": _draw_scanner, "exoskeleton": _draw_exoskeleton, "nanoswarm": _draw_nanoswarm,
    "cyberdeck": _draw_cyberdeck, "glitch": _draw_glitch, "uplink": _draw_uplink,
}

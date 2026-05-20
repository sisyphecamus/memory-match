"""Nature-themed illustration functions for Memory Match cards."""

import math
import random
from PIL import Image as PILImage

NATURE_SYMBOLS = [
    "oak_leaf", "mushroom", "acorn", "butterfly", "bloom",
    "pine_tree", "berries", "bird", "fern", "snail",
    "feather", "sunflower", "ladybug", "maple_leaf", "dragonfly",
    "tulip", "owl", "rose",
]


def draw_nature(draw, cx, cy, s, name, color):
    """Draw a nature illustration."""
    drawer = _DRAWERS.get(name)
    if drawer:
        drawer(draw, cx, cy, s, color)
    else:
        draw.ellipse([cx - s * 0.5, cy - s * 0.5, cx + s * 0.5, cy + s * 0.5], fill=color)


def _draw_oak_leaf(draw, cx, cy, s, color):
    pts = []
    for i in range(40):
        a = math.radians(i * 9 - 90)
        wave = 1.0 + 0.25 * math.sin(i * 1.2)
        r = s * wave
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.7))
    draw.polygon(pts, fill=color)
    draw.line([(cx, cy + s * 0.55), (cx, cy + s * 0.85)], fill=color, width=max(2, int(s * 0.08)))
    draw.line([(cx, cy - s * 0.6), (cx, cy + s * 0.5)], fill=(255, 255, 255, 80), width=1)
    for side in [-1, 1]:
        for vy in [cy - s * 0.2, cy, cy + s * 0.2]:
            draw.line([(cx, vy), (cx + side * s * 0.5, vy)], fill=(255, 255, 255, 60), width=1)


def _draw_mushroom(draw, cx, cy, s, color):
    stem_w = s * 0.2
    draw.rounded_rectangle([cx - stem_w, cy - s * 0.05, cx + stem_w, cy + s * 0.6], radius=int(stem_w * 0.8), fill=color)
    draw.ellipse([cx - s * 0.8, cy - s * 0.7, cx + s * 0.8, cy + s * 0.15], fill=color)
    draw.ellipse([cx - s * 0.65, cy - s * 0.05, cx + s * 0.65, cy + s * 0.25], fill=(255, 255, 255, 60))
    for sx, sy, sr in [(cx - s * 0.3, cy - s * 0.35, s * 0.12), (cx + s * 0.2, cy - s * 0.2, s * 0.1), (cx - s * 0.05, cy - s * 0.5, s * 0.08)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255, 180))


def _draw_acorn(draw, cx, cy, s, color):
    draw.ellipse([cx - s * 0.4, cy - s * 0.05, cx + s * 0.4, cy + s * 0.7], fill=color)
    draw.ellipse([cx - s * 0.5, cy - s * 0.4, cx + s * 0.5, cy + s * 0.1], fill=color)
    for i in range(-2, 3):
        lx = cx + i * s * 0.12
        draw.arc([lx - s * 0.1, cy - s * 0.35, lx + s * 0.1, cy + s * 0.05], start=200, end=340, fill=None, width=1)
    draw.line([(cx, cy - s * 0.35), (cx, cy - s * 0.6)], fill=color, width=max(2, int(s * 0.07)))
    draw.ellipse([cx - s * 0.15, cy + s * 0.1, cx + s * 0.05, cy + s * 0.35], fill=(255, 255, 255, 50))


def _draw_butterfly(draw, cx, cy, s, color):
    for side in [-1, 1]:
        sx = cx + side * s * 0.15
        ex = sx + side * s * 0.7
        x1, x2 = (sx, ex) if sx < ex else (ex, sx)
        draw.ellipse([x1, cy - s * 0.75, x2, cy], fill=color)
        ex2 = sx + side * s * 0.5
        x1b, x2b = (sx, ex2) if sx < ex2 else (ex2, sx)
        draw.ellipse([x1b, cy + s * 0.05, x2b, cy + s * 0.55], fill=color)
        spot_x1 = sx + side * s * 0.2
        spot_x2 = sx + side * s * 0.45
        if spot_x1 > spot_x2:
            spot_x1, spot_x2 = spot_x2, spot_x1
        draw.ellipse([spot_x1, cy - s * 0.35, spot_x2, cy - s * 0.1], fill=(255, 255, 255, 130))
    draw.ellipse([cx - s * 0.06, cy - s * 0.6, cx + s * 0.06, cy + s * 0.5], fill=color)
    for side in [-1, 1]:
        draw.line([(cx, cy - s * 0.55), (cx + side * s * 0.3, cy - s * 0.85)], fill=color, width=1)


def _draw_bloom(draw, cx, cy, s, color):
    for i in range(5):
        a = math.radians(i * 72 - 90)
        px = cx + s * 0.55 * math.cos(a)
        py = cy + s * 0.55 * math.sin(a)
        draw.ellipse([px - s * 0.35, py - s * 0.45, px + s * 0.35, py + s * 0.45], fill=color)
    draw.ellipse([cx - s * 0.2, cy - s * 0.2, cx + s * 0.2, cy + s * 0.2], fill=(255, 255, 200, 180))
    for _ in range(6):
        dx = random.randint(int(-s * 0.1), int(s * 0.1))
        dy = random.randint(int(-s * 0.1), int(s * 0.1))
        draw.ellipse([cx + dx - 1, cy + dy - 1, cx + dx + 1, cy + dy + 1], fill=color)


def _draw_pine_tree(draw, cx, cy, s, color):
    tw = s * 0.08
    draw.rectangle([cx - tw, cy + s * 0.3, cx + tw, cy + s * 0.8], fill=color)
    for h, w in [(0.6, 0.8), (0.35, 0.65), (0.1, 0.5)]:
        top_y = cy + s * (h - 0.65)
        base_y = top_y + s * 0.4
        draw.polygon([(cx, top_y - s * 0.05), (cx + s * w, base_y), (cx - s * w, base_y)], fill=color)


def _draw_berries(draw, cx, cy, s, color):
    draw.line([(cx, cy - s * 0.7), (cx, cy)], fill=color, width=max(2, int(s * 0.06)))
    positions = [(cx - s * 0.25, cy + s * 0.1, s * 0.22), (cx + s * 0.2, cy + s * 0.05, s * 0.2),
                 (cx - s * 0.05, cy + s * 0.35, s * 0.25), (cx + s * 0.3, cy + s * 0.3, s * 0.18),
                 (cx - s * 0.3, cy + s * 0.4, s * 0.18), (cx + s * 0.1, cy + s * 0.55, s * 0.2)]
    for bx, by, br in positions:
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=color)
        draw.ellipse([bx - br * 0.3, by - br * 0.4, bx + br * 0.1, by - br * 0.05], fill=(255, 255, 255, 70))
    lx, ly = cx + s * 0.35, cy - s * 0.15
    draw.ellipse([lx - s * 0.25, ly - s * 0.12, lx + s * 0.25, ly + s * 0.12], fill=color)


def _draw_bird(draw, cx, cy, s, color):
    draw.ellipse([cx - s * 0.45, cy - s * 0.3, cx + s * 0.35, cy + s * 0.25], fill=color)
    draw.ellipse([cx + s * 0.2, cy - s * 0.5, cx + s * 0.55, cy - s * 0.05], fill=color)
    draw.polygon([(cx + s * 0.5, cy - s * 0.3), (cx + s * 0.75, cy - s * 0.2), (cx + s * 0.5, cy - s * 0.15)], fill=color)
    draw.ellipse([cx + s * 0.38, cy - s * 0.4, cx + s * 0.46, cy - s * 0.32], fill=(255, 255, 255, 200))
    draw.polygon([(cx - s * 0.4, cy - s * 0.05), (cx - s * 0.7, cy - s * 0.25), (cx - s * 0.45, cy + s * 0.1)], fill=color)
    draw.line([(cx - s * 0.7, cy + s * 0.3), (cx + s * 0.6, cy + s * 0.4)], fill=color, width=max(2, int(s * 0.08)))
    for fx in [cx - s * 0.05, cx + s * 0.15]:
        draw.line([(fx, cy + s * 0.2), (fx, cy + s * 0.3)], fill=color, width=1)


def _draw_fern(draw, cx, cy, s, color):
    for i in range(30):
        a = math.radians(i * 5.5 - 90)
        r = s * (i / 30) * 0.85
        px = cx + r * math.cos(a)
        py = cy + r * math.sin(a)
        if i > 0:
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=color)
    for i in range(5, 25):
        a = math.radians(i * 5.5 - 90)
        r = s * (i / 30) * 0.85
        bx = cx + r * math.cos(a)
        by = cy + r * math.sin(a)
        for side in [-1, 1]:
            la = a + side * 0.7
            draw.line([(bx, by), (bx + s * 0.15 * math.cos(la), by + s * 0.15 * math.sin(la))], fill=color, width=1)


def _draw_snail(draw, cx, cy, s, color):
    draw.ellipse([cx - s * 0.6, cy + s * 0.2, cx + s * 0.3, cy + s * 0.6], fill=color)
    draw.ellipse([cx - s * 0.2, cy - s * 0.5, cx + s * 0.5, cy + s * 0.3], fill=color)
    for deg in range(0, 360, 5):
        r_spiral = s * 0.3 * (1 - deg / 400)
        a = math.radians(deg * 2)
        px = cx + s * 0.15 + r_spiral * math.cos(a)
        py = cy + r_spiral * math.sin(a)
        draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 255, 255, 100))
    for side in [-1, 1]:
        draw.line([(cx + s * 0.25, cy - s * 0.15), (cx + side * s * 0.4, cy - s * 0.55)], fill=color, width=1)


def _draw_feather(draw, cx, cy, s, color):
    draw.line([(cx, cy - s * 0.8), (cx, cy + s * 0.7)], fill=color, width=max(2, int(s * 0.06)))
    for side in [-1, 1]:
        pts = []
        for i in range(18):
            frac = i / 18
            y = cy - s * 0.75 + frac * s * 1.45
            w = s * 0.48 * (1 - abs(frac - 0.45) * 1.8) * max(0.1, (1 - frac))
            pts.append((cx + side * w, y))
        pts.append((cx, cy + s * 0.7))
        draw.polygon(pts, fill=color)
    for i in range(3, 15):
        frac = i / 18
        y = cy - s * 0.75 + frac * s * 1.45
        w = s * 0.4 * (1 - abs(frac - 0.45) * 1.8) * max(0.1, (1 - frac))
        for side in [-1, 1]:
            draw.line([(cx, y), (cx + side * w * 0.7, y)], fill=(255, 255, 255, 45), width=1)


def _draw_sunflower(draw, cx, cy, s, color):
    for i in range(16):
        a = math.radians(i * 22.5 - 90)
        px = cx + s * 0.55 * math.cos(a)
        py = cy + s * 0.55 * math.sin(a)
        petal_pts = [(cx + s * 0.2 * math.cos(a - 0.15), cy + s * 0.2 * math.sin(a - 0.15)),
                     (px + s * 0.12 * math.cos(a - 0.05), py + s * 0.12 * math.sin(a - 0.05)),
                     (px + s * 0.15 * math.cos(a), py + s * 0.15 * math.sin(a)),
                     (px + s * 0.12 * math.cos(a + 0.05), py + s * 0.12 * math.sin(a + 0.05)),
                     (cx + s * 0.2 * math.cos(a + 0.15), cy + s * 0.2 * math.sin(a + 0.15))]
        draw.polygon(petal_pts, fill=color)
    draw.ellipse([cx - s * 0.25, cy - s * 0.25, cx + s * 0.25, cy + s * 0.25], fill=(50, 35, 20, 200))


def _draw_ladybug(draw, cx, cy, s, color):
    draw.ellipse([cx - s * 0.45, cy - s * 0.2, cx + s * 0.45, cy + s * 0.4], fill=color)
    draw.ellipse([cx - s * 0.15, cy - s * 0.5, cx + s * 0.15, cy - s * 0.2], fill=color)
    draw.line([(cx, cy - s * 0.3), (cx, cy + s * 0.35)], fill=(0, 0, 0, 60), width=1)
    for sx, sy in [(cx - s * 0.2, cy - s * 0.1), (cx + s * 0.2, cy - s * 0.05), (cx - s * 0.15, cy + s * 0.15), (cx + s * 0.25, cy + s * 0.15)]:
        draw.ellipse([sx - s * 0.08, sy - s * 0.08, sx + s * 0.08, sy + s * 0.08], fill=(0, 0, 0, 150))
    for side in [-1, 1]:
        draw.line([(cx + side * s * 0.08, cy - s * 0.45), (cx + side * s * 0.3, cy - s * 0.7)], fill=color, width=1)


def _draw_maple_leaf(draw, cx, cy, s, color):
    pts = []
    for i in range(5):
        a_base = math.radians(i * 72 - 90)
        pts.append((cx + s * 0.95 * math.cos(a_base), cy + s * 0.95 * math.sin(a_base)))
        pts.append((cx + s * 0.4 * math.cos(a_base + 0.22), cy + s * 0.4 * math.sin(a_base + 0.22)))
        pts.append((cx + s * 0.55 * math.cos(a_base + 0.35), cy + s * 0.55 * math.sin(a_base + 0.35)))
        pts.append((cx + s * 0.4 * math.cos(a_base - 0.22), cy + s * 0.4 * math.sin(a_base - 0.22)))
    draw.polygon(pts, fill=color)
    draw.line([(cx, cy + s * 0.3), (cx, cy + s * 0.8)], fill=color, width=max(2, int(s * 0.07)))
    for i in range(5):
        a = math.radians(i * 72 - 90)
        draw.line([(cx, cy), (cx + s * 0.7 * math.cos(a), cy + s * 0.7 * math.sin(a))], fill=(255, 255, 255, 55), width=1)


def _draw_dragonfly(draw, cx, cy, s, color):
    draw.ellipse([cx - s * 0.05, cy - s * 0.3, cx + s * 0.05, cy + s * 0.6], fill=color)
    draw.ellipse([cx - s * 0.12, cy - s * 0.45, cx + s * 0.12, cy - s * 0.25], fill=color)
    for side in [-1, 1]:
        ex1 = cx + side * s * 0.05
        ex2 = cx + side * s * 0.14
        if ex1 > ex2:
            ex1, ex2 = ex2, ex1
        draw.ellipse([ex1, cy - s * 0.42, ex2, cy - s * 0.32], fill=(255, 255, 255, 150))
    for side in [-1, 1]:
        for w_y, w_len in [(cy - s * 0.2, s * 0.8), (cy - s * 0.05, s * 0.7)]:
            wx1 = cx + side * s * 0.02
            wx2 = cx + side * s * 0.02 + side * w_len
            if wx1 > wx2:
                wx1, wx2 = wx2, wx1
            draw.ellipse([wx1, w_y - s * 0.08, wx2, w_y + s * 0.08], fill=color)
            draw.line([(cx, w_y), (cx + side * w_len * 0.8, w_y)], fill=(255, 255, 255, 50), width=1)


def _draw_tulip(draw, cx, cy, s, color):
    draw.line([(cx, cy + s * 0.15), (cx, cy + s * 0.8)], fill=color, width=max(2, int(s * 0.08)))
    draw.ellipse([cx - s * 0.5, cy + s * 0.25, cx, cy + s * 0.65], fill=color)
    draw.ellipse([cx, cy + s * 0.25, cx + s * 0.5, cy + s * 0.65], fill=color)
    draw.ellipse([cx - s * 0.25, cy - s * 0.1, cx + s * 0.25, cy + s * 0.2], fill=color)
    for angle in [-0.3, 0, 0.3]:
        px = cx + s * 0.2 * math.sin(angle)
        py = cy - s * 0.3
        draw.ellipse([px - s * 0.18, py - s * 0.5, px + s * 0.18, py + s * 0.15], fill=color)
    draw.line([(cx, cy - s * 0.55), (cx, cy - s * 0.1)], fill=(255, 255, 255, 40), width=1)


def _draw_owl(draw, cx, cy, s, color):
    draw.ellipse([cx - s * 0.55, cy + s * 0.1, cx + s * 0.55, cy + s * 0.7], fill=color)
    draw.ellipse([cx - s * 0.5, cy - s * 0.4, cx + s * 0.5, cy + s * 0.25], fill=color)
    for side in [-1, 1]:
        draw.polygon([(cx + side * s * 0.35, cy - s * 0.3), (cx + side * s * 0.5, cy - s * 0.7), (cx + side * s * 0.15, cy - s * 0.3)], fill=color)
    for side in [-1, 1]:
        ed_x1 = cx + side * s * 0.2
        ed_x2 = cx + side * s * 0.45
        if ed_x1 > ed_x2:
            ed_x1, ed_x2 = ed_x2, ed_x1
        draw.ellipse([ed_x1, cy - s * 0.2, ed_x2, cy + s * 0.1], fill=(255, 255, 255, 100))
        ep_x1 = cx + side * s * 0.28
        ep_x2 = cx + side * s * 0.38
        if ep_x1 > ep_x2:
            ep_x1, ep_x2 = ep_x2, ep_x1
        draw.ellipse([ep_x1, cy - s * 0.13, ep_x2, cy + s * 0.02], fill=(0, 0, 0, 180))
    draw.polygon([(cx - s * 0.06, cy + s * 0.05), (cx + s * 0.06, cy + s * 0.05), (cx, cy + s * 0.18)], fill=color)
    for i in range(3):
        fy = cy + s * 0.3 + i * s * 0.1
        draw.arc([cx - s * 0.35, fy - s * 0.05, cx + s * 0.35, fy + s * 0.05], start=10, end=170, fill=None, width=1)


def _draw_rose(draw, cx, cy, s, color):
    for i in range(5):
        a = math.radians(i * 72)
        px = cx + s * 0.4 * math.cos(a)
        py = cy + s * 0.4 * math.sin(a)
        draw.ellipse([px - s * 0.3, py - s * 0.25, px + s * 0.3, py + s * 0.25], fill=color)
    for i in range(5):
        a = math.radians(i * 72 + 36)
        px = cx + s * 0.2 * math.cos(a)
        py = cy + s * 0.2 * math.sin(a)
        draw.ellipse([px - s * 0.2, py - s * 0.18, px + s * 0.2, py + s * 0.18], fill=color)
    for deg in range(0, 400, 8):
        r_spiral = s * 0.12 * (deg / 400)
        a = math.radians(deg * 1.8)
        px = cx + r_spiral * math.cos(a)
        py = cy + r_spiral * math.sin(a)
        draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 255, 255, 100))
    draw.ellipse([cx + s * 0.3, cy + s * 0.3, cx + s * 0.6, cy + s * 0.5], fill=color)


_DRAWERS = {
    "oak_leaf": _draw_oak_leaf, "mushroom": _draw_mushroom, "acorn": _draw_acorn,
    "butterfly": _draw_butterfly, "bloom": _draw_bloom, "pine_tree": _draw_pine_tree,
    "berries": _draw_berries, "bird": _draw_bird, "fern": _draw_fern,
    "snail": _draw_snail, "feather": _draw_feather, "sunflower": _draw_sunflower,
    "ladybug": _draw_ladybug, "maple_leaf": _draw_maple_leaf, "dragonfly": _draw_dragonfly,
    "tulip": _draw_tulip, "owl": _draw_owl, "rose": _draw_rose,
}

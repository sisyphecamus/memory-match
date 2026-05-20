"""Card rendering with PIL — generates card face and back images."""

import math
import random
from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk

from .themes import to_roman
from .symbols import draw_symbol, NATURE_SYMBOLS, CYBERPUNK_SYMBOLS, VAPORWAVE_SYMBOLS

_FONT_BASE = "/Users/lemon/.claude/skills/canvas-design/canvas-fonts"


def _draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


class CardRenderer:
    """Generates and caches card images for a given theme and grid size."""

    def __init__(self, theme_cfg, rows, cols, dpi_scale=2):
        self.theme = theme_cfg
        self.rows = rows
        self.cols = cols
        self.scale = dpi_scale

        max_w = max(700 // cols, 70)
        max_h = max(500 // rows, 90)
        card_w = min(max_w, 130)
        card_h = min(int(card_w * 1.45), 190)
        card_w = max(card_w, 70)
        card_h = max(card_h, 100)

        self.card_w = card_w * dpi_scale
        self.card_h = card_h * dpi_scale
        self.disp_w = card_w
        self.disp_h = card_h
        self.radius = int(self.card_w * 0.12)

        self._back_img = None
        self._face_cache = {}

    def render_card_back(self):
        if self._back_img:
            return self._back_img

        w, h, r = self.card_w, self.card_h, self.radius
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        colors = self.theme["card_colors"]
        _draw_rounded_rect(draw, [0, 0, w, h], r, fill=colors["back_base"])
        _draw_rounded_rect(draw, [4, 4, w - 4, h - 4], r - 2, fill=None,
                           outline=colors["back_border"], width=3)
        pattern_name = self.theme.get("pattern", "dots")
        self._draw_pattern(draw, w, h, colors["back_pattern"], pattern_name)
        self._back_img = img
        return img

    def _draw_pattern(self, draw, w, h, color, pattern_name):
        if pattern_name == "daisies":
            step = int(w / 5)
            for x in range(step, w - step // 2, step):
                for y in range(step, h - step // 2, step):
                    self._draw_flower(draw, x, y, step // 3, color)
        elif pattern_name == "tree_of_life":
            self._draw_tree_of_life(draw, w, h, color)
        elif pattern_name == "hex_chip":
            self._draw_hex_chip(draw, w, h, color)
        elif pattern_name == "vaporwave":
            # Sunset gradient bands
            band_colors = [
                (255, 107, 157, 200),  # pink
                (180, 77, 255, 160),   # purple
                (0, 212, 255, 140),    # cyan
                (77, 124, 255, 100),   # blue
            ]
            band_h = h // len(band_colors)
            for i, bc in enumerate(band_colors):
                draw.rectangle([0, i * band_h, w, (i + 1) * band_h], fill=bc)
            # Sun circle
            import random as _rnd
            sun_x = int(w * 0.55)
            sun_y = int(h * 0.4)
            sun_r = int(min(w, h) * 0.18)
            draw.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r],
                         fill=(255, 107, 53, 180))
            # Palm tree
            px = int(w * 0.2)
            py_base = int(h * 0.75)
            py_top = int(h * 0.25)
            draw.line([(px, py_base), (px, py_top)], fill=(0, 0, 0, 120), width=3)
            for a_idx in range(5):
                angle = math.radians(-130 + a_idx * 30)
                length = min(w, h) * 0.18
                ex = px + length * math.cos(angle)
                ey = py_top + length * math.sin(angle)
                draw.line([(px, py_top), (ex, ey)], fill=(0, 0, 0, 100), width=2)
            # Grid floor
            grid_top = int(h * 0.7)
            for i in range(6):
                x = i * w // 5
                draw.line([(int(w * 0.5), grid_top), (x, h)], fill=(255, 255, 255, 40), width=1)
            for i in range(4):
                frac = 0.3 + i * 0.2
                gy = grid_top + int(frac * (h - grid_top))
                spread = int(frac * w * 0.35)
                draw.line([(int(w * 0.5) - spread, gy), (int(w * 0.5) + spread, gy)],
                          fill=(255, 255, 255, 50), width=1)
        elif pattern_name == "leaves":
            import random as _rnd
            for _ in range(12):
                x = _rnd.randint(int(w * 0.15), int(w * 0.85))
                y = _rnd.randint(int(h * 0.15), int(h * 0.85))
                a = _rnd.uniform(0, 2 * math.pi)
                sz = _rnd.randint(8, 18)
                self._draw_leaf(draw, x, y, sz, a, color)
        else:
            step = int(w / 6)
            for x in range(step, w, step):
                for y in range(step, h, step):
                    r_small = max(2, int(self.radius * 0.3))
                    draw.ellipse([x - r_small, y - r_small, x + r_small, y + r_small], fill=color)

    def _draw_tree_of_life(self, draw, w, h, color):
        """Symmetrical Tree of Life with vine border — Nature card back."""
        cx, cy = w // 2, h // 2
        gold = (212, 175, 55, 180)
        tree_color = color

        # Ornate vine border frame
        border_m = int(min(w, h) * 0.06)
        for pt in range(0, 360, 12):
            a = math.radians(pt)
            rx = cx + (w // 2 - border_m) * math.cos(a)
            ry = cy + (h // 2 - border_m) * math.sin(a)
            br = int(min(w, h) * 0.03)
            draw.ellipse([rx - br, ry - br, rx + br, ry + br],
                         fill=gold if pt % 24 == 0 else tree_color)
        # Connecting vine lines
        for pt in range(0, 360, 6):
            a1 = math.radians(pt)
            a2 = math.radians(pt + 6)
            x1 = cx + (w // 2 - border_m - 4) * math.cos(a1)
            y1 = cy + (h // 2 - border_m - 4) * math.sin(a1)
            x2 = cx + (w // 2 - border_m - 4) * math.cos(a2)
            y2 = cy + (h // 2 - border_m - 4) * math.sin(a2)
            draw.line([(x1, y1), (x2, y2)], fill=tree_color, width=1)

        # Tree trunk
        trunk_w = int(min(w, h) * 0.03)
        draw.rectangle([cx - trunk_w, cy, cx + trunk_w, cy + int(h * 0.3)],
                       fill=tree_color)
        # Trunk roots
        for side in [-1, 1]:
            for j in range(2):
                rx = cx + side * trunk_w
                ry = cy + int(h * 0.15) + j * int(h * 0.08)
                ex = cx + side * int(w * 0.08 + j * w * 0.03)
                ey = cy + int(h * 0.25 + j * h * 0.05)
                draw.line([(rx, ry), (ex, ey)], fill=tree_color, width=2)

        # Circular canopy — radiating branches
        for i in range(8):
            a = math.radians(i * 45 - 90)
            br_len = min(w, h) * 0.25
            ex = cx + br_len * math.cos(a)
            ey = cy - int(h * 0.05) + br_len * math.sin(a)
            draw.line([(cx, cy), (ex, ey)], fill=tree_color, width=max(2, int(min(w, h) * 0.02)))
            # Sub-branches
            for frac in [0.5, 0.75]:
                bx = cx + frac * (ex - cx)
                by = cy + frac * (ey - cy)
                for side in [-1, 1]:
                    sa = a + side * 0.5
                    sl = br_len * 0.18
                    sx = bx + sl * math.cos(sa)
                    sy = by + sl * math.sin(sa)
                    draw.line([(bx, by), (sx, sy)], fill=tree_color, width=1)

        # Leaf clusters at branch ends
        for i in range(8):
            a = math.radians(i * 45 - 90)
            br_len = min(w, h) * 0.25
            lx = cx + br_len * math.cos(a)
            ly = cy - int(h * 0.05) + br_len * math.sin(a)
            for _ in range(3):
                la = a + (random.random() - 0.5) * 0.6
                lr = br_len * 0.12 * random.random()
                lpx = lx + lr * math.cos(la)
                lpy = ly + lr * math.sin(la)
                ls = int(min(w, h) * 0.04)
                leaf_pts = [
                    (lpx, lpy - ls), (lpx + ls // 2, lpy), (lpx, lpy + ls), (lpx - ls // 2, lpy)
                ]
                draw.polygon(leaf_pts, fill=tree_color if random.random() > 0.3 else gold)

        # Glow dots in canopy
        for _ in range(12):
            ga = random.random() * 2 * math.pi
            gr = min(w, h) * 0.12 * random.random()
            gx = cx + gr * math.cos(ga)
            gy = cy - int(h * 0.05) + gr * math.sin(ga)
            gs = max(1, int(min(w, h) * 0.012))
            draw.ellipse([gx - gs, gy - gs, gx + gs, gy + gs], fill=gold)

    def _draw_hex_chip(self, draw, w, h, color):
        """Symmetrical hexagonal chip with circuit traces — Cyberpunk card back."""
        cx, cy = w // 2, h // 2
        neon_pink = (233, 69, 96, 200)
        neon_cyan = (0, 212, 255, 200)
        neon_blue = (77, 124, 255, 200)

        # Geometric light-track border
        border_m = int(min(w, h) * 0.05)
        for pt in range(0, 360, 15):
            a = math.radians(pt)
            ix = cx + (w // 2 - border_m) * math.cos(a)
            iy = cy + (h // 2 - border_m) * math.sin(a)
            # Corner nodes (more prominent)
            is_corner = pt % 45 == 0
            nr = int(min(w, h) * (0.025 if is_corner else 0.012))
            node_col = neon_pink if is_corner else neon_cyan
            draw.ellipse([ix - nr, iy - nr, ix + nr, iy + nr], fill=node_col)
            # Small connecting dashes between nodes
            if pt % 15 == 0 and not is_corner:
                a2 = math.radians(pt + 7.5)
                dx = cx + (w // 2 - border_m + 3) * math.cos(a2)
                dy = cy + (h // 2 - border_m + 3) * math.sin(a2)
                draw.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill=neon_cyan)

        # Central hex chip
        hex_r = min(w, h) * 0.18
        hex_pts = []
        for i in range(6):
            a = math.radians(i * 60 - 30)
            hex_pts.append((cx + hex_r * math.cos(a), cy + hex_r * math.sin(a)))
        draw.polygon(hex_pts, fill=(10, 10, 20, 220), outline=neon_cyan, width=2)

        # Inner hex details
        inner_r = hex_r * 0.55
        inner_pts = []
        for i in range(6):
            a = math.radians(i * 60 - 30)
            inner_pts.append((cx + inner_r * math.cos(a), cy + inner_r * math.sin(a)))
        draw.polygon(inner_pts, fill=None, outline=neon_pink, width=1)
        # Center dot
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=neon_cyan)
        # Diagonal lines in inner hex
        for i in range(3):
            a1 = math.radians(i * 120 - 30)
            a2 = math.radians(i * 120 + 180 - 30)
            draw.line(
                [(cx + inner_r * 0.3 * math.cos(a1), cy + inner_r * 0.3 * math.sin(a1)),
                 (cx + inner_r * 0.3 * math.cos(a2), cy + inner_r * 0.3 * math.sin(a2))],
                fill=neon_cyan, width=1,
            )

        # Radiating circuit traces
        for i in range(12):
            a = math.radians(i * 30)
            start_r = hex_r + 4
            end_r = min(w, h) * 0.35
            sx = cx + start_r * math.cos(a)
            sy = cy + start_r * math.sin(a)
            # Angular trace — step outward
            for step in range(3):
                sr = start_r + (end_r - start_r) * (step / 3)
                er = start_r + (end_r - start_r) * ((step + 0.8) / 3)
                sa = a + (0.1 if step % 2 == 0 else -0.1)
                trace_x1 = cx + sr * math.cos(sa)
                trace_y1 = cy + sr * math.sin(sa)
                trace_x2 = cx + er * math.cos(sa)
                trace_y2 = cy + er * math.sin(sa)
                trace_color = neon_cyan if step % 2 == 0 else neon_blue
                draw.line([(trace_x1, trace_y1), (trace_x2, trace_y2)],
                          fill=trace_color, width=1)
            # Node at end of trace
            ex = cx + end_r * math.cos(a)
            ey = cy + end_r * math.sin(a)
            enr = 3
            draw.ellipse([ex - enr, ey - enr, ex + enr, ey + enr], fill=neon_pink)

        # Small geometric dots scattered symmetrically
        for i in range(8):
            a = math.radians(i * 45 + 22.5)
            r = min(w, h) * 0.28
            dx = cx + r * math.cos(a)
            dy = cy + r * math.sin(a)
            draw.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=neon_blue)

    def _draw_flower(self, draw, cx, cy, size, color):
        for i in range(5):
            a = math.radians(i * 72)
            px = cx + size * 0.6 * math.cos(a)
            py = cy + size * 0.6 * math.sin(a)
            draw.ellipse([px - size * 0.4, py - size * 0.4, px + size * 0.4, py + size * 0.4], fill=color)
        draw.ellipse([cx - size * 0.25, cy - size * 0.25, cx + size * 0.25, cy + size * 0.25], fill=color)

    def _draw_leaf(self, draw, cx, cy, size, angle, color):
        leaf = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
        leaf_draw = ImageDraw.Draw(leaf)
        pts = [(size, 0), (size + size // 3, size), (size, size * 2), (size - size // 3, size)]
        leaf_draw.polygon(pts, fill=color)
        leaf_draw.line([(size, 0), (size, size * 2)], fill=color, width=1)
        rotated = leaf.rotate(math.degrees(angle), resample=Image.BICUBIC, center=(size, size))
        img = draw._image
        img.paste(rotated, (cx - size, cy - size), rotated)

    def render_card_face(self, symbol_id):
        if symbol_id in self._face_cache:
            return self._face_cache[symbol_id]

        w, h, r = self.card_w, self.card_h, self.radius
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        colors = self.theme["card_colors"]
        border_color = colors.get("face_border", colors.get("back_border", "#999"))

        _draw_rounded_rect(draw, [0, 0, w, h], r, fill=colors["face_base"])

        # Minimal border
        border_margin = int(min(w, h) * 0.03)
        _draw_rounded_rect(
            draw, [border_margin, border_margin, w - border_margin, h - border_margin],
            max(r - 2, 4), fill=None, outline=border_color, width=2,
        )

        # Roman numeral index — top-left
        idx = to_roman(symbol_id + 1)
        try:
            idx_font_size = max(12, int(w * 0.115))
            idx_font = ImageFont.truetype(f"{_FONT_BASE}/CrimsonPro-Bold.ttf", size=idx_font_size)
            draw.text((int(w * 0.065), int(h * 0.045)), idx, fill=border_color, font=idx_font)
        except Exception:
            pass

        # Illustration area
        ill_pad_h = int(h * 0.08)
        ill_y1 = border_margin + ill_pad_h
        ill_y2 = h - border_margin - int(h * 0.15)
        ill_x_pad = int(w * 0.12)
        ill_w = w - ill_x_pad * 2
        ill_h = ill_y2 - ill_y1

        theme_name = self.theme.get("name", "Nature")
        if theme_name == "Cyberpunk":
            symbol_list = CYBERPUNK_SYMBOLS
        elif theme_name == "Vaporwave":
            symbol_list = VAPORWAVE_SYMBOLS
        else:
            symbol_list = NATURE_SYMBOLS
        symbol_name = symbol_list[symbol_id % len(symbol_list)]
        symbol_size = int(min(ill_w, ill_h) * 0.55)
        draw_symbol(draw, w // 2, ill_y1 + ill_h // 2, symbol_size, symbol_name, colors["symbol"], theme_name)

        # Label
        label = symbol_name.replace("_", " ").title()
        try:
            label_font_size = max(10, int(h * 0.075))
            label_font = ImageFont.truetype(f"{_FONT_BASE}/Outfit-Bold.ttf", size=label_font_size)
            bbox = draw.textbbox((0, 0), label, font=label_font)
            text_w = bbox[2] - bbox[0]
            label_y = ill_y2 + int(h * 0.015)
            draw.text((w // 2 - text_w // 2, label_y), label, fill=border_color, font=label_font)
        except Exception:
            pass

        self._face_cache[symbol_id] = img
        return img

    def to_ctk_image(self, pil_image):
        return ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(self.disp_w, self.disp_h))

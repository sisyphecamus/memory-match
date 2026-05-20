"""Main menu frame for Memory Match v2.0."""

import math
import customtkinter as ctk
from PIL import Image, ImageDraw
from ..themes import THEMES, DIFFICULTIES
from ..leaderboard import get_all_scores


def _make_nature_bg(w, h):
    """Generate a subtle leaf-vein textured background for Nature theme."""
    img = Image.new("RGBA", (w, h), (23, 38, 27, 255))
    draw = ImageDraw.Draw(img)
    # Subtle vein-like arcs
    for _ in range(6):
        cx = w // 2 + (hash(str(_ * 37)) % (w // 2)) - w // 4
        cy = h // 2 + (hash(str(_ * 73)) % (h // 2)) - h // 4
        for deg in range(0, 360, 15):
            a = math.radians(deg)
            r1 = 40 + (hash(str(_ * 17 + deg)) % 80)
            r2 = r1 + 30
            x1 = cx + r1 * math.cos(a)
            y1 = cy + r1 * math.sin(a)
            x2 = cx + r2 * math.cos(a + 0.3)
            y2 = cy + r2 * math.sin(a + 0.3)
            draw.line([(x1, y1), (x2, y2)], fill=(52, 99, 52, 40), width=1)
    return img


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()

        theme = THEMES[self.app.selected_theme]
        self.configure(fg_color=theme["bg"])

        # Nature theme: add subtle vein background
        if self.app.selected_theme == "Nature":
            self._bg_label = ctk.CTkLabel(self, text="")
            self._bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.update_idletasks()
            w = self.winfo_width() or 900
            h = self.winfo_height() or 800
            bg_img = _make_nature_bg(w, h)
            ctk_img = ctk.CTkImage(light_image=bg_img, dark_image=bg_img, size=(w, h))
            self._bg_label.configure(image=ctk_img)

        ctk.CTkLabel(
            self, text="Memory Match",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color=theme["accent"],
        ).pack(pady=(100, 10))

        ctk.CTkLabel(
            self, text="Flip cards. Find pairs. Win.",
            font=ctk.CTkFont(size=16), text_color=theme["text"],
        ).pack(pady=(0, 50))

        ctk.CTkLabel(
            self, text="Difficulty",
            font=ctk.CTkFont(size=14, weight="bold"), text_color=theme["text"],
        ).pack()
        diff_menu = ctk.CTkOptionMenu(
            self, values=list(DIFFICULTIES.keys()), command=self._set_difficulty,
            fg_color=theme["card_colors"]["back_base"], text_color=theme["text"],
            button_color=theme["accent"], button_hover_color=theme["card_colors"]["back_pattern"],
            font=ctk.CTkFont(size=14),
        )
        diff_menu.set(self.app.selected_difficulty)
        diff_menu.pack(pady=(5, 20))

        ctk.CTkLabel(
            self, text="Theme",
            font=ctk.CTkFont(size=14, weight="bold"), text_color=theme["text"],
        ).pack()
        theme_menu = ctk.CTkOptionMenu(
            self, values=list(THEMES.keys()), command=self._set_theme,
            fg_color=theme["card_colors"]["back_base"], text_color=theme["text"],
            button_color=theme["accent"], button_hover_color=theme["card_colors"]["back_pattern"],
            font=ctk.CTkFont(size=14),
        )
        theme_menu.set(self.app.selected_theme)
        theme_menu.pack(pady=(5, 20))

        ctk.CTkButton(
            self, text="Start Game", command=self.app.start_game,
            fg_color=theme["accent"], hover_color=theme["card_colors"]["back_pattern"],
            text_color="#FFFFFF", font=ctk.CTkFont(size=18, weight="bold"),
            width=200, height=55, corner_radius=27,
        ).pack(pady=(20, 15))

        ctk.CTkButton(
            self, text="Leaderboard", command=self._show_leaderboard,
            fg_color=theme["card_colors"]["back_base"], text_color=theme["text"],
            hover_color=theme["card_colors"]["back_border"],
            font=ctk.CTkFont(size=14),
            width=160, height=40, corner_radius=20,
        ).pack()

    def _set_difficulty(self, value):
        self.app.selected_difficulty = value

    def _set_theme(self, value):
        self.app.selected_theme = value
        ctk.set_appearance_mode(THEMES[value]["mode"])
        self.refresh()

    def _show_leaderboard(self):
        theme = THEMES[self.app.selected_theme]
        colors = theme["card_colors"]
        data = get_all_scores()

        dlg = ctk.CTkToplevel(self)
        dlg.title("Leaderboard")
        dlg.geometry("480x460")
        dlg.resizable(False, False)
        dlg.configure(fg_color=theme["bg"])
        dlg.transient(self)
        dlg.grab_set()
        dlg.update_idletasks()
        px = self.winfo_rootx() + (self.winfo_width() - 480) // 2
        py = self.winfo_rooty() + (self.winfo_height() - 460) // 2
        dlg.geometry(f"+{px}+{py}")

        ctk.CTkLabel(
            dlg, text="Leaderboard",
            font=ctk.CTkFont(size=24, weight="bold"), text_color=theme["accent"],
        ).pack(pady=(20, 10))

        if not data:
            ctk.CTkLabel(
                dlg, text="No scores yet. Play a game!",
                font=ctk.CTkFont(size=16), text_color=theme["text"],
            ).pack(pady=60)
        else:
            scroll_frame = ctk.CTkScrollableFrame(dlg, fg_color="transparent",
                                                  width=440, height=340)
            scroll_frame.pack(fill="both", padx=20, pady=10, expand=True)

            for t_name in sorted(data.keys()):
                t_data = data[t_name]
                ctk.CTkLabel(
                    scroll_frame, text=t_name,
                    font=ctk.CTkFont(size=16, weight="bold"), text_color=theme["accent"],
                ).pack(anchor="w", pady=(10, 4))

                for diff_name in sorted(t_data.keys()):
                    entry = t_data[diff_name]
                    mm = entry["time_seconds"] // 60
                    ss = entry["time_seconds"] % 60
                    score_text = f"{entry['score']}"

                    row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                    row.pack(fill="x", pady=2)
                    ctk.CTkLabel(
                        row, text=f"  {diff_name}",
                        font=ctk.CTkFont(size=13), text_color=theme["text"], width=120,
                    ).pack(side="left")
                    ctk.CTkLabel(
                        row, text=score_text,
                        font=ctk.CTkFont(size=13, weight="bold"), text_color=theme["accent"], width=70,
                    ).pack(side="left")
                    ctk.CTkLabel(
                        row, text=f"{mm:02d}:{ss:02d}  |  {entry['moves']} moves",
                        font=ctk.CTkFont(size=12), text_color=theme["text"], width=150,
                    ).pack(side="left")

        ctk.CTkButton(
            dlg, text="Close", command=dlg.destroy,
            fg_color=theme["card_colors"]["back_base"], text_color=theme["text"],
            hover_color=theme["card_colors"]["back_border"],
            font=ctk.CTkFont(size=14),
            width=100, height=35, corner_radius=15,
        ).pack(pady=15)

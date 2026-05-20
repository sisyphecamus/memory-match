"""Victory screen frame for Memory Match v2.0."""

import time
import customtkinter as ctk

from ..themes import THEMES
from ..game_logic import calculate_score
from ..leaderboard import record_score


class VictoryFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()

        theme = THEMES[self.app.selected_theme]
        self.configure(fg_color=theme["bg"])

        elapsed = int(time.time() - self.app.game_start_time)
        mm = elapsed // 60
        ss = elapsed % 60
        board_size = max(self.app.rows, self.app.cols)
        score = calculate_score(self.app.moves, elapsed, board_size)

        record_score(
            self.app.selected_theme, self.app.selected_difficulty,
            score, self.app.moves, elapsed,
        )

        ctk.CTkLabel(
            self, text="You Win!",
            font=ctk.CTkFont(size=40, weight="bold"), text_color=theme["accent"],
        ).pack(pady=(80, 30))

        stats = [
            ("Moves", str(self.app.moves)),
            ("Time", f"{mm:02d}:{ss:02d}"),
            ("Score", str(score)),
        ]
        for label, value in stats:
            row_frame = ctk.CTkFrame(self, fg_color="transparent")
            row_frame.pack(pady=6)
            ctk.CTkLabel(
                row_frame, text=f"{label}:  ", font=ctk.CTkFont(size=20), text_color=theme["text"],
            ).pack(side="left")
            ctk.CTkLabel(
                row_frame, text=value,
                font=ctk.CTkFont(size=20, weight="bold"), text_color=theme["accent"],
            ).pack(side="left")

        ctk.CTkButton(
            self, text="Play Again", command=self.app.start_game,
            fg_color=theme["accent"], hover_color=theme["card_colors"]["back_pattern"],
            text_color="#FFFFFF", font=ctk.CTkFont(size=16, weight="bold"),
            width=180, height=45, corner_radius=22,
        ).pack(pady=(40, 10))

        ctk.CTkButton(
            self, text="Main Menu", command=lambda: self.app.show_frame("MenuFrame"),
            fg_color=theme["card_colors"]["back_base"],
            hover_color=theme["card_colors"]["back_pattern"],
            text_color=theme["text"], font=ctk.CTkFont(size=14),
            width=140, height=40, corner_radius=20,
        ).pack()

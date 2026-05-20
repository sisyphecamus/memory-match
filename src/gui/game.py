"""Game board frame for Memory Match v2.0."""

import time
import customtkinter as ctk

from ..themes import THEMES
from ..game_logic import check_match, is_game_won


class GameFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._after_id = None

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        if self._after_id:
            self.after_cancel(self._after_id)

        theme = THEMES[self.app.selected_theme]
        self.configure(fg_color=theme["bg"])

        # Top bar
        top = ctk.CTkFrame(self, fg_color=theme["card_colors"]["back_base"], corner_radius=12)
        top.pack(fill="x", padx=20, pady=(20, 10), ipady=8)

        self.timer_label = ctk.CTkLabel(
            top, text="00:00", font=ctk.CTkFont(size=18, weight="bold"), text_color=theme["text"],
        )
        self.timer_label.pack(side="left", padx=30)

        ctk.CTkLabel(
            top, text=f"{self.app.selected_theme}  |  {self.app.selected_difficulty}",
            font=ctk.CTkFont(size=14), text_color=theme["text"],
        ).pack(side="left")

        self.moves_label = ctk.CTkLabel(
            top, text="Moves: 0", font=ctk.CTkFont(size=18, weight="bold"), text_color=theme["text"],
        )
        self.moves_label.pack(side="right", padx=30)

        # Exit button — centered in top bar
        self.exit_btn = ctk.CTkButton(
            top, text="✕ Exit", command=self._confirm_exit,
            fg_color="transparent", text_color=theme["text"],
            hover_color=theme["accent"],
            font=ctk.CTkFont(size=14, weight="bold"),
            width=70, height=30, corner_radius=8,
        )
        self.exit_btn.place(relx=0.5, rely=0.5, anchor="center")

        # Card grid
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(expand=True, padx=10, pady=10)

        self.app.card_buttons = []
        rows, cols = self.app.rows, self.app.cols
        w_img = self.app.card_renderer.disp_w
        h_img = self.app.card_renderer.disp_h
        colors = theme["card_colors"]

        for r in range(rows):
            row_buttons = []
            grid_frame.grid_rowconfigure(r, weight=1, uniform="card")
            for c in range(cols):
                grid_frame.grid_columnconfigure(c, weight=1, uniform="card")
                btn = ctk.CTkButton(
                    grid_frame, text="", image=self.app.card_back_img,
                    fg_color=colors["back_base"], hover_color=colors["back_border"],
                    corner_radius=8, width=w_img, height=h_img,
                    command=lambda rr=r, cc=c: self._flip_card(rr, cc),
                )
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                row_buttons.append(btn)
            self.app.card_buttons.append(row_buttons)

        ctk.CTkButton(
            self, text="Main Menu", command=self._back_to_menu,
            fg_color="transparent", text_color=theme["text"],
            hover_color=theme["card_colors"]["back_base"], font=ctk.CTkFont(size=13),
        ).pack(pady=(5, 15))

        self._tick_timer()

    def _tick_timer(self):
        if self.app.game_start_time is None:
            return
        elapsed = int(time.time() - self.app.game_start_time)
        mm = elapsed // 60
        ss = elapsed % 60
        self.timer_label.configure(text=f"{mm:02d}:{ss:02d}")
        self._after_id = self.after(500, self._tick_timer)

    def _flip_card(self, row, col):
        if self.app.locked:
            return
        card = self.app.board[row][col]
        if card["status"] != "hidden":
            return

        card["status"] = "revealed"
        btn = self.app.card_buttons[row][col]
        theme = THEMES[self.app.selected_theme]
        colors = theme["card_colors"]

        btn.configure(image=self.app.card_face_imgs[card["content"]], fg_color=colors["face_base"])

        if self.app.sound:
            self.app.sound.play("flip")

        if self.app.first_flip is None:
            self.app.first_flip = (row, col)
            return

        self.app.moves += 1
        self.moves_label.configure(text=f"Moves: {self.app.moves}")
        self.app.locked = True

        r1, c1 = self.app.first_flip
        card1 = self.app.board[r1][c1]
        card2 = card

        if check_match(card1, card2):
            card1["status"] = "matched"
            card2["status"] = "matched"
            self.app.first_flip = None
            self.app.locked = False
            self._update_card_appearance(r1, c1)
            self._update_card_appearance(row, col)
            if self.app.sound:
                self.app.sound.play("match")
            if is_game_won(self.app.board):
                self.after(600, self.app.end_game)
        else:
            self.after(700, lambda: self._hide_cards(r1, c1, row, col))

    def _hide_cards(self, r1, c1, r2, c2):
        theme = THEMES[self.app.selected_theme]
        colors = theme["card_colors"]
        for r, c in [(r1, c1), (r2, c2)]:
            card = self.app.board[r][c]
            if card["status"] == "revealed":
                card["status"] = "hidden"
                btn = self.app.card_buttons[r][c]
                btn.configure(image=self.app.card_back_img, fg_color=colors["back_base"])
        if self.app.sound:
            self.app.sound.play("mismatch")
        self.app.first_flip = None
        self.app.locked = False

    def _update_card_appearance(self, row, col):
        card = self.app.board[row][col]
        btn = self.app.card_buttons[row][col]
        theme = THEMES[self.app.selected_theme]
        colors = theme["card_colors"]
        if card["status"] == "matched":
            btn.configure(
                image=self.app.card_face_imgs[card["content"]],
                fg_color=colors["back_border"], hover_color=colors["back_border"],
                state="disabled",
            )

    def _confirm_exit(self):
        theme = THEMES[self.app.selected_theme]
        colors = theme["card_colors"]
        dialog = ctk.CTkToplevel(self)
        dialog.title("Exit Game")
        dialog.geometry("320x160")
        dialog.resizable(False, False)
        dialog.configure(fg_color=theme["bg"])
        dialog.transient(self)
        dialog.grab_set()
        # Center on parent
        dialog.update_idletasks()
        px = self.winfo_rootx() + (self.winfo_width() - 320) // 2
        py = self.winfo_rooty() + (self.winfo_height() - 160) // 2
        dialog.geometry(f"+{px}+{py}")

        ctk.CTkLabel(
            dialog, text="Return to Main Menu?",
            font=ctk.CTkFont(size=16, weight="bold"), text_color=theme["text"],
        ).pack(pady=(30, 10))
        ctk.CTkLabel(
            dialog, text="Your current progress will be lost.",
            font=ctk.CTkFont(size=13), text_color=theme["text"],
        ).pack(pady=(0, 20))

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack()
        ctk.CTkButton(
            btn_frame, text="Cancel",
            command=dialog.destroy,
            fg_color=colors["back_base"], text_color=theme["text"],
            hover_color=colors["back_pattern"], font=ctk.CTkFont(size=14),
            width=100, height=35, corner_radius=10,
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            btn_frame, text="Exit",
            command=lambda: self._do_exit(dialog),
            fg_color=theme["accent"], text_color="#FFFFFF",
            hover_color=colors["back_pattern"], font=ctk.CTkFont(size=14, weight="bold"),
            width=100, height=35, corner_radius=10,
        ).pack(side="left", padx=10)

    def _do_exit(self, dialog):
        dialog.destroy()
        self._back_to_menu()

    def _back_to_menu(self):
        self.app.game_start_time = None
        if self._after_id:
            self.after_cancel(self._after_id)
        self.app.show_frame("MenuFrame")

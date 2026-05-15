import random
import time
import customtkinter as ctk

EMOJIS = [
    "🎮", "🎯", "🎨", "🎵", "🚀", "🌟", "💎", "🔥",
    "🎪", "🍀", "🌈", "🦊", "🐼", "🦄", "🍕", "⚡",
    "🎸", "🌙", "🍭", "🎲", "🪐", "🐙", "🍒", "👻",
]

THEMES = {
    "Pastel": {
        "card_back": "#FFD6E0",
        "bg": "#FFF5F5",
        "card_revealed": "#FFE4EC",
        "accent": "#FF8FAB",
        "text": "#5C3D4A",
        "card_hover": "#FFC2D4",
        "mode": "light",
    },
    "Cyberpunk": {
        "card_back": "#1A1A2E",
        "bg": "#0F0F23",
        "card_revealed": "#16213E",
        "accent": "#E94560",
        "text": "#EAEAEA",
        "card_hover": "#222244",
        "mode": "dark",
    },
    "Nature": {
        "card_back": "#D4E7C5",
        "bg": "#F1F8E8",
        "card_revealed": "#BFD8AF",
        "accent": "#99BC85",
        "text": "#3D4F38",
        "card_hover": "#C8DFB8",
        "mode": "light",
    },
}

DIFFICULTIES = {
    "Easy (4×4)": (4, 4),
    "Medium (4×6)": (4, 6),
    "Hard (6×6)": (6, 6),
}


# ── Pure Logic Functions (testable) ──────────────────────────────

def create_board(rows, cols=None, theme="Pastel"):
    """Generate a shuffled board of paired cards.

    Args:
        rows: Number of rows in the grid.
        cols: Number of columns (defaults to rows for square board).
        theme: Visual theme name (does not affect logic).

    Returns:
        2D list of card dicts, each with id, content, and status.
    """
    if cols is None:
        cols = rows

    total_cards = rows * cols
    if total_cards % 2 != 0:
        raise ValueError("Board must have an even number of cards.")

    pair_count = total_cards // 2
    selected = EMOJIS[:pair_count]

    cards = []
    for pid, emoji in enumerate(selected):
        cards.append({"id": pid, "content": emoji, "status": "hidden"})
        cards.append({"id": pid, "content": emoji, "status": "hidden"})

    random.shuffle(cards)

    board = []
    for r in range(rows):
        board.append(cards[r * cols : (r + 1) * cols])

    return board


def check_match(card1, card2):
    """Return True if two cards have the same id."""
    return card1["id"] == card2["id"]


def calculate_score(moves, elapsed_seconds, size):
    """Calculate score based on moves, time, and board size.

    Lower moves and faster time yield higher scores.
    """
    total_pairs = size * size // 2
    base_score = size * size * 50
    move_penalty = max(0, (moves - total_pairs) * 5)
    time_penalty = int(elapsed_seconds * 0.3)
    score = max(1, base_score - move_penalty - time_penalty)
    return score


def is_game_won(board):
    """Return True if every card on the board has status 'matched'."""
    for row in board:
        for card in row:
            if card["status"] != "matched":
                return False
    return True


# ── GUI Application ──────────────────────────────────────────────

class MemoryMatchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Memory Match")
        self.geometry("800x700")
        self.minsize(600, 500)

        self.selected_theme = "Pastel"
        self.selected_difficulty = "Easy (4×4)"
        self.board = None
        self.rows = 4
        self.cols = 4
        self.moves = 0
        self.first_flip = None
        self.game_start_time = None
        self.card_buttons = []
        self.locked = False

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for FrameClass in (MenuFrame, GameFrame, VictoryFrame):
            frame = FrameClass(self.container, self)
            self.frames[FrameClass.__name__] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_frame("MenuFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.refresh()
        frame.tkraise()

    def apply_theme_colors(self):
        theme = THEMES[self.selected_theme]
        ctk.set_appearance_mode(theme["mode"])

    def start_game(self):
        self.apply_theme_colors()
        self.rows, self.cols = DIFFICULTIES[self.selected_difficulty]
        self.board = create_board(self.rows, self.cols, self.selected_theme)
        self.moves = 0
        self.first_flip = None
        self.game_start_time = time.time()
        self.card_buttons = []
        self.locked = False
        self.show_frame("GameFrame")

    def end_game(self):
        self.show_frame("VictoryFrame")


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()

        theme = THEMES[self.app.selected_theme]
        self.configure(fg_color=theme["bg"])

        ctk.CTkLabel(
            self, text="🃏 Memory Match", font=ctk.CTkFont(size=42, weight="bold"),
            text_color=theme["accent"],
        ).pack(pady=(80, 10))

        ctk.CTkLabel(
            self, text="Flip cards. Find pairs. Win.",
            font=ctk.CTkFont(size=16), text_color=theme["text"],
        ).pack(pady=(0, 50))

        ctk.CTkLabel(
            self, text="Difficulty", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=theme["text"],
        ).pack()
        diff_menu = ctk.CTkOptionMenu(
            self, values=list(DIFFICULTIES.keys()),
            command=self._set_difficulty,
            fg_color=theme["card_back"], text_color=theme["text"],
            button_color=theme["accent"], button_hover_color=theme["card_hover"],
            font=ctk.CTkFont(size=14),
        )
        diff_menu.set(self.app.selected_difficulty)
        diff_menu.pack(pady=(5, 20))

        ctk.CTkLabel(
            self, text="Theme", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=theme["text"],
        ).pack()
        theme_menu = ctk.CTkOptionMenu(
            self, values=list(THEMES.keys()),
            command=self._set_theme,
            fg_color=theme["card_back"], text_color=theme["text"],
            button_color=theme["accent"], button_hover_color=theme["card_hover"],
            font=ctk.CTkFont(size=14),
        )
        theme_menu.set(self.app.selected_theme)
        theme_menu.pack(pady=(5, 40))

        ctk.CTkButton(
            self, text="Start Game", command=self.app.start_game,
            fg_color=theme["accent"], hover_color=theme["card_hover"],
            text_color="#FFFFFF" if theme["mode"] == "dark" else "#FFFFFF",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=200, height=50, corner_radius=25,
        ).pack()

    def _set_difficulty(self, value):
        self.app.selected_difficulty = value

    def _set_theme(self, value):
        self.app.selected_theme = value
        ctk.set_appearance_mode(THEMES[value]["mode"])
        self.refresh()


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
        top = ctk.CTkFrame(self, fg_color=theme["card_back"], corner_radius=12)
        top.pack(fill="x", padx=20, pady=(20, 10), ipady=8)

        self.timer_label = ctk.CTkLabel(
            top, text="⏱ 00:00", font=ctk.CTkFont(size=18, weight="bold"),
            text_color=theme["text"],
        )
        self.timer_label.pack(side="left", padx=30)

        ctk.CTkLabel(
            top, text=f"{self.app.selected_theme}  |  {self.app.selected_difficulty}",
            font=ctk.CTkFont(size=14), text_color=theme["text"],
        ).pack(side="left")

        self.moves_label = ctk.CTkLabel(
            top, text="Moves: 0", font=ctk.CTkFont(size=18, weight="bold"),
            text_color=theme["text"],
        )
        self.moves_label.pack(side="right", padx=30)

        # Card grid
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(expand=True, padx=20, pady=10)

        self.app.card_buttons = []
        rows, cols = self.app.rows, self.app.cols

        for r in range(rows):
            row_buttons = []
            grid_frame.grid_rowconfigure(r, weight=1, uniform="card")
            for c in range(cols):
                grid_frame.grid_columnconfigure(c, weight=1, uniform="card")
                card = self.app.board[r][c]
                btn = ctk.CTkButton(
                    grid_frame,
                    text="?",
                    font=ctk.CTkFont(size=28),
                    fg_color=theme["card_back"],
                    hover_color=theme["card_hover"],
                    text_color=theme["text"],
                    corner_radius=10,
                    width=80,
                    height=80,
                    command=lambda rr=r, cc=c: self._flip_card(rr, cc),
                )
                btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                row_buttons.append(btn)
            self.app.card_buttons.append(row_buttons)

        # Back button
        ctk.CTkButton(
            self, text="← Main Menu", command=self._back_to_menu,
            fg_color="transparent", text_color=theme["text"],
            hover_color=theme["card_back"], font=ctk.CTkFont(size=13),
        ).pack(pady=(5, 15))

        self._tick_timer()

    def _tick_timer(self):
        if self.app.game_start_time is None:
            return
        elapsed = int(time.time() - self.app.game_start_time)
        mm = elapsed // 60
        ss = elapsed % 60
        self.timer_label.configure(text=f"⏱ {mm:02d}:{ss:02d}")
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
        btn.configure(text=card["content"], fg_color=theme["card_revealed"])

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
            if is_game_won(self.app.board):
                self.after(600, self.app.end_game)
        else:
            self.after(
                700,
                lambda: self._hide_cards(r1, c1, row, col),
            )

    def _hide_cards(self, r1, c1, r2, c2):
        theme = THEMES[self.app.selected_theme]
        for r, c in [(r1, c1), (r2, c2)]:
            card = self.app.board[r][c]
            if card["status"] == "revealed":
                card["status"] = "hidden"
                btn = self.app.card_buttons[r][c]
                btn.configure(text="?", fg_color=theme["card_back"])
        self.app.first_flip = None
        self.app.locked = False

    def _update_card_appearance(self, row, col):
        card = self.app.board[row][col]
        btn = self.app.card_buttons[row][col]
        theme = THEMES[self.app.selected_theme]
        if card["status"] == "matched":
            btn.configure(
                text=card["content"],
                fg_color=theme["accent"],
                hover_color=theme["accent"],
                state="disabled",
                text_color_disabled=theme["text"],
            )
        else:
            btn.configure(
                text=card["content"],
                fg_color=theme["card_revealed"],
                state="normal",
            )

    def _back_to_menu(self):
        self.app.game_start_time = None
        if self._after_id:
            self.after_cancel(self._after_id)
        self.app.show_frame("MenuFrame")


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

        ctk.CTkLabel(
            self, text="🎉 You Win!",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color=theme["accent"],
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
                row_frame, text=f"{label}:  ",
                font=ctk.CTkFont(size=20), text_color=theme["text"],
            ).pack(side="left")
            ctk.CTkLabel(
                row_frame, text=value,
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=theme["accent"],
            ).pack(side="left")

        ctk.CTkButton(
            self, text="Play Again",
            command=self.app.start_game,
            fg_color=theme["accent"], hover_color=theme["card_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=180, height=45, corner_radius=22,
        ).pack(pady=(40, 10))

        ctk.CTkButton(
            self, text="Main Menu",
            command=lambda: self.app.show_frame("MenuFrame"),
            fg_color=theme["card_back"], hover_color=theme["card_hover"],
            text_color=theme["text"],
            font=ctk.CTkFont(size=14),
            width=140, height=40, corner_radius=20,
        ).pack()


def main():
    app = MemoryMatchApp()
    app.mainloop()


if __name__ == "__main__":
    main()

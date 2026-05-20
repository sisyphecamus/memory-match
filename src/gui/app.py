"""Main application class for Memory Match v2.0."""

import time
import customtkinter as ctk

from ..themes import THEMES, DIFFICULTIES
from ..game_logic import create_board
from ..sound import SoundManager
from ..card_renderer import CardRenderer

from .menu import MenuFrame
from .game import GameFrame
from .victory import VictoryFrame


class MemoryMatchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Memory Match")
        self.geometry("900x800")
        self.minsize(700, 600)

        self.selected_theme = "Vaporwave"
        self.selected_difficulty = "Easy (4×4)"
        self.board = None
        self.rows = 4
        self.cols = 4
        self.moves = 0
        self.first_flip = None
        self.game_start_time = None
        self.card_buttons = []
        self.locked = False
        self.card_renderer = None
        self.card_back_img = None
        self.card_face_imgs = None
        self.sound = None

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

        if self.sound is None:
            try:
                self.sound = SoundManager()
            except Exception:
                self.sound = None

        theme_cfg = THEMES[self.selected_theme]
        self.card_renderer = CardRenderer(theme_cfg, self.rows, self.cols)
        self.card_back_img = self.card_renderer.to_ctk_image(
            self.card_renderer.render_card_back()
        )
        pair_count = self.rows * self.cols // 2
        self.card_face_imgs = {}
        for pid in range(pair_count):
            face_pil = self.card_renderer.render_card_face(pid)
            self.card_face_imgs[pid] = self.card_renderer.to_ctk_image(face_pil)

        self.show_frame("GameFrame")

    def end_game(self):
        if self.sound:
            self.sound.play("victory")
        self.show_frame("VictoryFrame")

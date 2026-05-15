# Memory Match

#### Video Demo: <URL HERE>

#### Description:

Memory Match is a card-flipping memory game built with Python and CustomTkinter. The player reveals cards two at a time, trying to find all matching pairs on the board. It combines classic memory-testing gameplay with a modern, polished graphical user interface featuring three visual themes and three difficulty levels.

The game starts with a main menu where the player can choose a difficulty — Easy (4x4 grid, 8 pairs), Medium (4x6 grid, 12 pairs), or Hard (6x6 grid, 18 pairs) — and a visual theme: Pastel with soft pink tones, Cyberpunk with deep navy and neon accents, or Nature with calm green hues. Once the game begins, a timer starts counting up, a move counter tracks every pair flip attempt, and the board is displayed as a grid of face-down cards marked with "?". Clicking a card reveals its hidden emoji. The player then clicks a second card; if the two emoji match, the pair stays revealed with a highlighted accent color. If they do not match, both cards flip back after a brief pause. The game ends when every pair has been matched, at which point a victory screen displays the final stats — total moves, elapsed time, and a calculated score.

The architecture cleanly separates pure game logic from the graphical interface. The functions `create_board`, `check_match`, `calculate_score`, and `is_game_won` are defined at the top level of project.py with no dependency on any GUI library. This design makes the core game rules independently testable with pytest. The GUI layer is implemented as a MemoryMatchApp class (with MenuFrame, GameFrame, and VictoryFrame subclasses) using CustomTkinter widgets. The app calls the logic functions to drive game state, but the functions themselves remain framework-agnostic.

The scoring formula rewards both accuracy and speed. The base score scales with board size, and penalties are subtracted for excess moves beyond the theoretical minimum and for elapsed time. A perfect game — matching every pair on the first attempt — yields the highest possible score for a given board size.

#### Files

- **project.py**: Contains the four core logic functions (`create_board`, `check_match`, `calculate_score`, `is_game_won`), the `main()` entry point, and the full CustomTkinter GUI application (MemoryMatchApp, MenuFrame, GameFrame, VictoryFrame). The GUI manages card rendering, timer updates, the two-step flip state machine, theme switching, and screen transitions.

- **test_project.py**: Contains 17 pytest test cases across four test classes (TestCreateBoard, TestCheckMatch, TestCalculateScore, TestIsGameWon). Tests verify board dimensions, card pairing, shuffling randomness, match detection correctness, score calculations including edge cases, and victory condition detection.

- **requirements.txt**: Lists the single external dependency, `customtkinter`, a library that provides modern, themed Tkinter widgets with rounded corners, hover effects, and built-in dark/light mode support.

#### Design Choices

CustomTkinter was chosen over Pygame or vanilla Tkinter because it offers a modern look out of the box — rounded buttons, smooth hover states, and appearance mode switching — while remaining lightweight enough for a card game. Pygame would have provided more animation control, but for a turn-based memory game, the extra complexity was not justified.

The card data model uses a simple dictionary (`{"id": int, "content": str, "status": str}`) rather than a class to keep the logic functions lightweight and easily testable. Each card's `id` uniquely identifies its pair, the `content` holds the display emoji, and `status` tracks whether the card is hidden, revealed, or matched. This flat structure makes board serialization and state inspection trivial during testing.

The two-flip state machine uses a `locked` flag to prevent the player from flipping a third card while a pair is being evaluated. A 700-millisecond delay before hiding non-matching cards gives the player enough time to see both cards while keeping the gameplay pace brisk. Matched cards are rendered in the theme's accent color and disabled to prevent re-clicking.

The three visual themes are defined as dictionaries mapping color roles (card back, background, card revealed, accent, text, hover) to hex codes. This makes adding new themes as simple as adding a new dictionary entry. The theme switching mechanism rebuilds the current frame when changed, which keeps the implementation straightforward at the cost of a brief flicker — an acceptable trade-off for a project of this scope.

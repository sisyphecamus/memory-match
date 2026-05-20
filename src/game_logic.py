# Memory Match v2.0 — Game Logic (pure functions, framework-agnostic)

import random

EMOJIS = [
    "🎮", "🎯", "🎨", "🎵", "🚀", "🌟", "💎", "🔥",
    "🎪", "🍀", "🌈", "🦊", "🐼", "🦄", "🍕", "⚡",
    "🎸", "🌙", "🍭", "🎲", "🪐", "🐙", "🍒", "👻",
]


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

    cards = []
    for pid in range(pair_count):
        cards.append({"id": pid, "content": pid, "status": "hidden"})
        cards.append({"id": pid, "content": pid, "status": "hidden"})

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

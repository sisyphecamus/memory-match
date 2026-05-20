"""Leaderboard — persistent high-score tracking for Memory Match."""

import os
import json
from datetime import datetime

LEADERBOARD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "leaderboard.json")


def _load():
    """Load leaderboard data from disk."""
    if os.path.exists(LEADERBOARD_PATH):
        try:
            with open(LEADERBOARD_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def _save(data):
    """Persist leaderboard data to disk."""
    with open(LEADERBOARD_PATH, "w") as f:
        json.dump(data, f, indent=2)


def record_score(theme, difficulty, score, moves, elapsed_seconds):
    """Record a score for the given theme + difficulty combo.
    Only keeps the best score (highest) per combo.
    """
    data = _load()
    data.setdefault(theme, {})
    entry = {
        "score": score,
        "moves": moves,
        "time_seconds": elapsed_seconds,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    existing = data[theme].get(difficulty)
    if existing is None or score > existing["score"]:
        data[theme][difficulty] = entry
    _save(data)


def get_all_scores():
    """Return the full leaderboard dict: {theme: {difficulty: entry, ...}, ...}"""
    return _load()

import pytest
from project import create_board, check_match, calculate_score, is_game_won


class TestCreateBoard:
    def test_dimensions(self):
        for size in [4, 6]:
            board = create_board(size)
            assert len(board) == size
            for row in board:
                assert len(row) == size

    def test_all_cards_hidden(self):
        board = create_board(4)
        for row in board:
            for card in row:
                assert card["status"] == "hidden"

    def test_pairs_exist(self):
        board = create_board(4)
        ids = [card["id"] for row in board for card in row]
        for pid in set(ids):
            assert ids.count(pid) == 2

    def test_cards_shuffled(self):
        boards = [create_board(6) for _ in range(5)]
        id_sequences = [
            tuple(card["id"] for row in b for card in row) for b in boards
        ]
        unique_sequences = set(id_sequences)
        assert len(unique_sequences) > 1

    def test_theme_param_accepted(self):
        board = create_board(4, theme="cyberpunk")
        assert len(board) == 4


class TestCheckMatch:
    def test_matching_cards(self):
        card1 = {"id": 1, "content": "🐼"}
        card2 = {"id": 1, "content": "🐼"}
        assert check_match(card1, card2) is True

    def test_non_matching_cards(self):
        card1 = {"id": 1, "content": "🐼"}
        card2 = {"id": 2, "content": "🦊"}
        assert check_match(card1, card2) is False

    def test_same_content_different_id(self):
        card1 = {"id": 1, "content": "🐼"}
        card2 = {"id": 2, "content": "🐼"}
        assert check_match(card1, card2) is False


class TestCalculateScore:
    def test_perfect_game(self):
        score = calculate_score(moves=8, elapsed_seconds=5, size=4)
        assert score >= 790

    def test_penalty_for_many_moves(self):
        perfect = calculate_score(moves=8, elapsed_seconds=10, size=4)
        sloppy = calculate_score(moves=30, elapsed_seconds=10, size=4)
        assert sloppy < perfect

    def test_penalty_for_slow_time(self):
        fast = calculate_score(moves=8, elapsed_seconds=5, size=4)
        slow = calculate_score(moves=8, elapsed_seconds=200, size=4)
        assert slow < fast

    def test_never_negative(self):
        score = calculate_score(moves=999, elapsed_seconds=9999, size=4)
        assert score >= 1

    def test_larger_board_higher_base(self):
        small = calculate_score(moves=8, elapsed_seconds=10, size=4)
        large = calculate_score(moves=18, elapsed_seconds=10, size=6)
        assert large > small


class TestIsGameWon:
    def test_all_matched(self):
        board = [
            [{"status": "matched"}, {"status": "matched"}],
            [{"status": "matched"}, {"status": "matched"}],
        ]
        assert is_game_won(board) is True

    def test_some_hidden(self):
        board = [
            [{"status": "matched"}, {"status": "hidden"}],
            [{"status": "matched"}, {"status": "matched"}],
        ]
        assert is_game_won(board) is False

    def test_some_revealed(self):
        board = [
            [{"status": "matched"}, {"status": "revealed"}],
            [{"status": "matched"}, {"status": "matched"}],
        ]
        assert is_game_won(board) is False

    def test_empty_board(self):
        assert is_game_won([]) is True

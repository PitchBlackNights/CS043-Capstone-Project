import unittest, os, files, pathlib
from board import Board
from copy import deepcopy


class TestBoardMethods(unittest.TestCase):
    def test_init_values(self):
        board: Board = Board()
        self.assertEqual(board.id, "")
        self.assertEqual(board.type, Board.Type.NONE)
        self.assertEqual(board.difficulty, Board.Difficulty.NONE)
        self.assertEqual(len(board.board), 9)
        self.assertEqual(board.generated, False)

    def test_serialize_empty(self):
        board: Board = Board()
        with self.assertRaises(Exception):
            _: str = board.serialize()

    def test_serialize_filled(self):
        board: Board = Board()
        board.generate(0)
        serial: str = board.serialize()
        expect_serial: str = (
            '{"id": "0", "type": 1, "difficulty": 0, "board": [["1", "3", "4", "6", "8", "2", "9", "5", "7"], ["2", "8", "7", "9", "5", "1", "6", "4", "3"], ["9", "6", "5", "7", "4", "3", "8", "1", "2"], ["5", "7", "2", "4", "1", "6", "3", "9", "8"], ["6", "4", "8", "3", "2", "9", "1", "7", "5"], ["3", "9", "1", "5", "7", "8", "4", "2", "6"], ["8", "1", "6", "2", "9", "7", "5", "3", "4"], ["7", "5", "3", "1", "6", "4", "2", "8", "9"], ["4", "2", "9", "8", "3", "5", "7", "6", "1"]]}'
        )
        self.assertEqual(serial, expect_serial)

    def test_serialize_game(self):
        board: Board = Board()
        board.generate(0)
        serial1: str = board.serialize()
        board.gameify(Board.Difficulty.EASY)
        serial2: str = board.serialize()
        self.assertNotEqual(serial1, serial2)

    def test_deserialize_filled(self):
        board: Board = Board()
        board.generate(0)
        serial: str = board.serialize()
        deserial: Board = Board()
        deserial.deserialize(serial)
        self.assertEqual(board, deserial)

    def test_deserialize_game(self):
        board: Board = Board()
        board.generate(0)
        board.gameify(Board.Difficulty.EASY)
        serial: str = board.serialize()
        deserial: Board = Board()
        deserial.deserialize(serial)
        self.assertEqual(board, deserial)

    def test_format_empty(self):
        self.maxDiff = None
        board: Board = Board()
        format: str = board.format()
        expect_format: str = (
            "╭───────┬───────┬───────╮\n│       │       │       │\n│       │       │       │\n│       │       │       │\n├───────┼───────┼───────┤\n│       │       │       │\n│       │       │       │\n│       │       │       │\n├───────┼───────┼───────┤\n│       │       │       │\n│       │       │       │\n│       │       │       │\n╰───────┴───────┴───────╯"
        )
        self.assertEqual(format, expect_format)

    def test_format_filled(self):
        self.maxDiff = None
        board: Board = Board()
        board.generate(0)
        format: str = board.format()
        expect_format: str = (
            "╭───────┬───────┬───────╮\n│ 1 3 4 │ 6 8 2 │ 9 5 7 │\n│ 2 8 7 │ 9 5 1 │ 6 4 3 │\n│ 9 6 5 │ 7 4 3 │ 8 1 2 │\n├───────┼───────┼───────┤\n│ 5 7 2 │ 4 1 6 │ 3 9 8 │\n│ 6 4 8 │ 3 2 9 │ 1 7 5 │\n│ 3 9 1 │ 5 7 8 │ 4 2 6 │\n├───────┼───────┼───────┤\n│ 8 1 6 │ 2 9 7 │ 5 3 4 │\n│ 7 5 3 │ 1 6 4 │ 2 8 9 │\n│ 4 2 9 │ 8 3 5 │ 7 6 1 │\n╰───────┴───────┴───────╯"
        )
        self.assertEqual(format, expect_format)

    def test_format_game(self):
        board: Board = Board()
        board.generate(0)
        format1: str = board.format()
        board.gameify(Board.Difficulty.EASY)
        format2: str = board.format()
        self.assertEqual(len(format1), len(format2))

        differences: int = 0
        for index in range(len(format1)):
            if format1[index] != format2[index]:
                differences += 1

        self.assertEqual(differences, 28)

    def test_gamify_easy(self):
        board: Board = Board()
        board.generate(0)
        board1: list[list[str]] = deepcopy(board.board)
        board.gameify(Board.Difficulty.EASY)
        board2: list[list[str]] = deepcopy(board.board)
        self.assertEqual(len(board1), len(board2))

        differences: int = 0
        for y in range(len(board1)):
            for x in range(len(board1[y])):
                if board1[y][x] != board2[y][x]:
                    differences += 1

        self.assertEqual(differences, 28)

    def test_gamify_medium(self):
        board: Board = Board()
        board.generate(0)
        board1: list[list[str]] = deepcopy(board.board)
        board.gameify(Board.Difficulty.MEDIUM)
        board2: list[list[str]] = deepcopy(board.board)
        self.assertEqual(len(board1), len(board2))

        differences: int = 0
        for y in range(len(board1)):
            for x in range(len(board1[y])):
                if board1[y][x] != board2[y][x]:
                    differences += 1

        self.assertEqual(differences, 37)

    def test_gamify_hard(self):
        board: Board = Board()
        board.generate(0)
        board1: list[list[str]] = deepcopy(board.board)
        board.gameify(Board.Difficulty.HARD)
        board2: list[list[str]] = deepcopy(board.board)
        self.assertEqual(len(board1), len(board2))

        differences: int = 0
        for y in range(len(board1)):
            for x in range(len(board1[y])):
                if board1[y][x] != board2[y][x]:
                    differences += 1

        self.assertEqual(differences, 46)

    def test_generate_determinism(self):
        board1: Board = Board()
        board1.generate(0)
        board2: Board = Board()
        board2.generate(0)
        self.assertEqual(board1.board, board2.board)

    def test_generate_integers_only(self):
        for seed in range(100):
            board: Board = Board()
            board.generate(seed)
            for y in range(len(board.board)):
                for x in range(len(board.board[y])):
                    try:
                        _: int = int(board.board[y][x])
                    except ValueError:
                        self.fail(
                            f"`Board.generate()` generated a non-integer value:\n    Val: '{board.board[y][x]}' ({x}, {y})\n    Seed: {seed}"
                        )


class TestBoardTypes(unittest.TestCase):
    def test_difficulty_str(self):
        self.assertEqual(str(Board.Difficulty.EASY), "Easy")
        self.assertEqual(str(Board.Difficulty.MEDIUM), "Medium")
        self.assertEqual(str(Board.Difficulty.HARD), "Hard")


def save_dir_helper() -> str:
    save_dir: str = os.path.abspath("./test_saved_boards")
    try:
        files.delete_path(save_dir)
    except FileNotFoundError:
        pass
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=False)
    return save_dir


class TestFilesMethods(unittest.TestCase):
    def test_load_saved_boards_empty(self):
        save_dir: str = save_dir_helper()

        saved_boards: list[Board] = files.load_saved_boards(save_dir=save_dir)
        self.assertEqual(saved_boards, [])

        files.delete_path(save_dir)

    def test_load_saved_boards(self):
        save_dir: str = save_dir_helper()

        with open(os.path.abspath(f"{save_dir}/0.board"), "x+") as file:
            file.write(
                '{"id": "0", "type": 1, "difficulty": 0, "board": [["1", "3", "4", "6", "8", "2", "9", "5", "7"], ["2", "8", "7", "9", "5", "1", "6", "4", "3"], ["9", "6", "5", "7", "4", "3", "8", "1", "2"], ["5", "7", "2", "4", "1", "6", "3", "9", "8"], ["6", "4", "8", "3", "2", "9", "1", "7", "5"], ["3", "9", "1", "5", "7", "8", "4", "2", "6"], ["8", "1", "6", "2", "9", "7", "5", "3", "4"], ["7", "5", "3", "1", "6", "4", "2", "8", "9"], ["4", "2", "9", "8", "3", "5", "7", "6", "1"]]}'
            )
        with open(os.path.abspath(f"{save_dir}/1.board"), "x+") as file:
            file.write(
                '{"id": "1", "type": 1, "difficulty": 0, "board": [["8", "4", "6", "5", "9", "3", "1", "2", "7"], ["9", "2", "3", "1", "4", "7", "8", "6", "5"], ["1", "5", "7", "2", "6", "8", "4", "9", "3"], ["3", "9", "1", "6", "7", "5", "2", "8", "4"], ["5", "7", "4", "8", "2", "9", "3", "1", "6"], ["6", "8", "2", "4", "3", "1", "7", "5", "9"], ["4", "6", "8", "3", "5", "2", "9", "7", "1"], ["7", "1", "5", "9", "8", "4", "6", "3", "2"], ["2", "3", "9", "7", "1", "6", "5", "4", "8"]]}'
            )
        with open(os.path.abspath(f"{save_dir}/0.txt"), "x+") as file:
            file.write("test")

        saved_boards: list[Board] = files.load_saved_boards(save_dir=save_dir)
        self.assertEqual(len(saved_boards), 2)

        files.delete_path(save_dir)

    def test_save_board_empty(self):
        save_dir: str = save_dir_helper()

        board: Board = Board()
        with self.assertRaises(Exception):
            files.save_board(board, save_dir=save_dir)

        files.delete_path(save_dir)

    def test_save_board_filled(self):
        save_dir: str = save_dir_helper()

        board: Board = Board()
        board.generate(0)
        files.save_board(board, save_dir=save_dir)
        expect_data: str = (
            '{"id": "0", "type": 1, "difficulty": 0, "board": [["1", "3", "4", "6", "8", "2", "9", "5", "7"], ["2", "8", "7", "9", "5", "1", "6", "4", "3"], ["9", "6", "5", "7", "4", "3", "8", "1", "2"], ["5", "7", "2", "4", "1", "6", "3", "9", "8"], ["6", "4", "8", "3", "2", "9", "1", "7", "5"], ["3", "9", "1", "5", "7", "8", "4", "2", "6"], ["8", "1", "6", "2", "9", "7", "5", "3", "4"], ["7", "5", "3", "1", "6", "4", "2", "8", "9"], ["4", "2", "9", "8", "3", "5", "7", "6", "1"]]}'
        )

        with open(os.path.abspath(f"{save_dir}/0.board"), "r") as file:
            self.assertEqual(file.read(), expect_data)

        files.delete_path(save_dir)

    def test_delete_board_none(self):
        save_dir: str = save_dir_helper()

        # Doesn't matter if board is generated or saved, cause the "`save_dir` is empty"
        # check happens before the "is generated" & "is saved" checks
        board: Board = Board()
        with self.assertRaises(
            Exception,
            msg="Called `files.delete_board()` when there are no boards actively saved!",
        ):
            files.delete_board(board, save_dir=save_dir)

        files.delete_path(save_dir)

    def test_delete_board_empty(self):
        save_dir: str = save_dir_helper()

        tmp_board: Board = Board()
        tmp_board.generate(100)
        files.save_board(tmp_board, save_dir=save_dir)

        board: Board = Board()
        with self.assertRaises(
            Exception,
            msg="Called `files.delete_board()` on a board the hasn't been generated!",
        ):
            files.delete_board(board, save_dir=save_dir)

        files.delete_path(save_dir)

    def test_delete_board_not_saved(self):
        save_dir: str = save_dir_helper()

        tmp_board: Board = Board()
        tmp_board.generate(100)
        files.save_board(tmp_board, save_dir=save_dir)

        board: Board = Board()
        board.generate(0)
        with self.assertRaises(
            Exception,
            msg="Called `files.delete_board()` on a board the hasn't been saved!",
        ):
            files.delete_board(board, save_dir=save_dir)

        files.delete_path(save_dir)

    def test_delete_board_correct(self):
        save_dir: str = save_dir_helper()

        tmp_board: Board = Board()
        tmp_board.generate(100)
        files.save_board(tmp_board, save_dir=save_dir)

        board: Board = Board()
        board.generate(0)
        files.save_board(board, save_dir=save_dir)
        files.delete_board(board, save_dir=save_dir)
        if "0.board" in files.get_all_saved_board_files(save_dir=save_dir):
            self.fail("`files.delete_board()` failed to delete the board!")

        files.delete_path(save_dir)


if __name__ == "__main__":
    unittest.main()

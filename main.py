# This is a Sudoku board generator that can generate filled
# boards and starting boards at 3 different levels.
#
# It makes use of a Wave Function Collapse algorithm to
# quickly, and accurately, generate valid Sudoku boards.


from board import Board
import files


tmp_board: Board = Board()
tmp_board.generate(100)
print(tmp_board.format())
print()

files.save_board(tmp_board)

saved_boards: list[Board] = files.load_saved_boards()
for board in saved_boards:
    print(f"ID: {board.id}")
    print(board.format())
    print()

# This is a Sudoku board generator that can generate filled
# boards and starting boards at 3 different levels.
#
# It makes use of a Wave Function Collapse algorithm to
# quickly, and accurately, generate valid Sudoku boards.


from board import Board


# BUG: Cell value sometimes collapses to None without triggering Exception
for cycle in range(10):
    board: Board = Board()
    board.generate(cycle)
    print(board.format())

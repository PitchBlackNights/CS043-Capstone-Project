# This is a Sudoku board generator that can generate filled
# boards and starting boards at 3 different levels.
#
# It makes use of a Wave Function Collapse algorithm to
# quickly, and accurately, generate valid Sudoku boards.


from board import Board


for cycle in range(10):
    board: Board = Board()
    board.generate(cycle)
    print(f"Seed: {cycle}")
    print(board.format())
    print("\n")

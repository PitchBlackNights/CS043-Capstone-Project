# This is a Sudoku board generator that can generate filled
# boards and starting boards at 3 different levels.
#
# It makes use of a Wave Function Collapse algorithm to
# quickly, and accurately, generate valid Sudoku boards.


from board import Board
from copy import deepcopy


board: Board = Board()
board.generate(100)
print(board.format())
print()

serialized: tuple[int, int, list[list[str]]] = board.serialize()
print(board.serialize())

deserialized: Board = Board()
deserialized.deserialize(serialized)
print(deserialized.format())


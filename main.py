# This is a Sudoku board generator that can generate filled
# boards and starting boards at 3 different levels.
#
# It makes use of a Wave Function Collapse algorithm to
# quickly, and accurately, generate valid Sudoku boards.


from board import Board
from ui import clear_screen, UI


clear_screen()
tmp_ui: UI = UI(
    title="Test",
    header=True,
    options=[("1", "Option 1"), ("2", "Option 2"), ("+", "Option +")],
)
tmp_ui.show()
print(f"USER CHOICE: {tmp_ui.get_choice()}")

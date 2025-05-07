# ======================================================================================
# PROJECT DESCRIPTION
# ======================================================================================
# This is a Sudoku board generator that can generate filled
# boards and starting boards at 3 different levels.
#
# It makes use of a Wave Function Collapse algorithm to
# quickly, and accurately, generate valid Sudoku boards.


# ======================================================================================
# CORE CONCEPTS
# ======================================================================================
# Core concept comments are prefixed with `CORE CONCEPT:`
#
# - Instance of a function with parameters    (main.py:423:1)
# - Instance of Try and Except    (files.py:36:5)
# - Instance of the `in` keyword    (ui.py:44:13)
# - Instance of a `tuple` or `list` with methods used on them    (board.py:86:17)
# - Instance of a 2D list    (board.py:57:9)
# - Instance of packing    (board.py:151:25)
# - Instance of unpacking    (board.py:156:13)
# - Instance of a dictionary    (serde.py:115:5)
# - Instance of comparing the equivalence of two items    (tests.py:118:9)
# - Instance of a hidden attribute    (board.py:59:9)


from board import Board
from ui import UI
import files, tools, math, time


# tools.clear_all_saved_boards()
# for cycle in range(0, 31):
#     tmp_board = Board()
#     tmp_board.generate(cycle)
#     files.save_board(tmp_board)
# for cycle in range(0, 31):
#     tmp_board = Board()
#     tmp_board.generate(cycle)
#     tmp_board.gameify(Board.Difficulty.MEDIUM)
#     files.save_board(tmp_board)
# input("DONE")


# Load saved boards into separate lists for filled and game boards
saved_boards: list[Board] = files.load_saved_boards()
filled_boards: list[Board] = []
game_boards: list[Board] = []

boards_per_page: int = 10


def update_board_lists() -> None:
    """Updates the lists keeping track of all the saved boards"""
    global saved_boards, filled_boards, game_boards
    saved_boards = files.load_saved_boards()
    filled_boards = []
    game_boards = []

    for board in saved_boards:
        if board.type == Board.Type.FULL:
            filled_boards.append(board)
        elif board.type == Board.Type.GAME:
            game_boards.append(board)


def main_menu() -> None:
    """Main menu loop"""
    while True:
        main_menu_ui: UI = UI(
            title="Main Menu",
            options=[("1", "View Boards"), ("2", "Generate Boards\n"), ("X", "Exit")],
        )
        main_menu_ui.show()
        user_choice: str = main_menu_ui.get_choice()

        # Handle user choice for the main menu
        # MAIN MENU: Exit
        if user_choice == "X":
            quit()

        # MAIN MENU: View Boards
        elif user_choice == "1":
            view_boards()

        # MAIN MENU: Generate Boards
        elif user_choice == "2":
            generate_boards()


def generate_boards() -> None:
    """Menu for generating boards"""
    # Update the saved boards lists to avoid undefined behavior
    update_board_lists()

    while True:
        generate_boards_ui: UI = UI(
            title="Generate Boards",
            options=[
                ("1", "Filled Boards"),
                ("2", "Game Boards\n"),
                ("B", "Back"),
                ("X", "Exit"),
            ],
        )
        generate_boards_ui.show()
        user_choice: str = generate_boards_ui.get_choice()

        # Handle user choice for the "Generate Boards" menu
        # GENERATE BOARDS: Exit
        if user_choice == "X":
            quit()

        # GENERATE BOARDS: Back
        elif user_choice == "B":
            return

        # GENERATE BOARDS: Filled Boards
        elif user_choice == "1":
            generate_boards__filled_boards()

        # GENERATE BOARDS: Filled Boards
        elif user_choice == "2":
            generate_boards__game_boards()


def generate_boards__filled_boards() -> None:
    """Menu for generating filled boards."""
    # Update the saved boards lists to avoid undefined behavior
    update_board_lists()

    # Prompt the user for the number of boards to generate
    num_to_gen: int = tools.get_int("Number of boards to generate (0 = Cancel): ")
    for cycle in range(num_to_gen):
        board = Board()  # Create a new board instance
        board.generate(Board.last_seed + 1)  # Generate a filled board with a new seed

        # Display the progress of board generation
        show_board_ui: UI = UI(
            title=f"Generating Boards ({cycle + 1}/{num_to_gen}...)",
        )
        show_board_ui.show()
        print(f"Board #{board.id}\n{board.format()}\n")

        # Display options for saving or skipping the generated board
        options_ui: UI = UI(
            header=False,
            options=[("1", "Save"), ("2", "Skip\n"), ("B", "Back"), ("X", "Exit")],
        )
        options_ui.show(clr_screen=False)
        user_choice: str = options_ui.get_choice()

        # Handle user choice for the generated board
        # GENERATE FILLED BOARDS: Exit
        if user_choice == "X":
            quit()

        # GENERATE FILLED BOARDS: Back
        elif user_choice == "B":
            return

        # GENERATE FILLED BOARDS: Skip
        elif user_choice == "2":
            continue

        # GENERATE FILLED BOARDS: Save
        elif user_choice == "1":
            files.save_board(board)
            print("Saved board!")
            time.sleep(1)


def generate_boards__game_boards() -> None:
    """Menu for generating game boards."""
    # Update the saved boards lists to avoid undefined behavior
    update_board_lists()

    # Prompt the user for the number of boards to generate
    num_to_gen: int = tools.get_int("Number of boards to generate (0 = Cancel): ")
    print("\nWhat difficulty level?")  # Ask the user for the difficulty level

    # Display difficulty options and get the user's choice
    options_ui: UI = UI(
        header=False,
        options=[("1", "Easy"), ("2", "Medium"), ("3", "Hard")],
    )
    options_ui.show(clr_screen=False)
    user_difficulty: Board.Difficulty = Board.Difficulty(int(options_ui.get_choice()))

    # Generate the specified number of boards
    for cycle in range(num_to_gen):
        board = Board()  # Create a new board instance
        board.generate(Board.last_seed + 1)  # Generate a filled board with a new seed
        board.gameify(
            user_difficulty
        )  # Convert the board into a game board with the chosen difficulty

        # Display the progress of board generation
        show_board_ui: UI = UI(
            title=f"Generating Boards ({cycle + 1}/{num_to_gen}...)",
        )
        show_board_ui.show()
        print(f"Board #{board.id} (DIFF: {str(board.difficulty)})\n{board.format()}\n")

        # Display options for saving or skipping the generated board
        options_ui: UI = UI(
            header=False,
            options=[("1", "Save"), ("2", "Skip\n"), ("B", "Back"), ("X", "Exit")],
        )
        options_ui.show(clr_screen=False)
        user_choice: str = options_ui.get_choice()

        # Handle user choice for the generated board
        # GENERATE GAME BOARDS: Exit
        if user_choice == "X":
            quit()

        # GENERATE GAME BOARDS: Back
        elif user_choice == "B":
            return

        # GENERATE GAME BOARDS: Skip
        elif user_choice == "2":
            continue

        # GENERATE GAME BOARDS: Save
        elif user_choice == "1":
            files.save_board(board)
            print("Saved board!")
            time.sleep(1)


def view_boards() -> None:
    """Menu for viewing saved boards"""
    # Update the saved boards lists to avoid undefined behavior
    update_board_lists()

    while True:
        view_boards_ui: UI = UI(
            title="View Boards",
            options=[
                ("1", "Filled Boards"),
                ("2", "Game Boards\n"),
                ("B", "Back"),
                ("X", "Exit"),
            ],
        )
        view_boards_ui.show()
        user_choice: str = view_boards_ui.get_choice()

        # VIEW BOARDS: Exit
        if user_choice == "X":
            quit()

        # VIEW BOARDS: Back
        elif user_choice == "B":
            return

        # VIEW BOARDS: Filled Boards
        elif user_choice == "1":
            view_boards__filled_boards()

        # VIEW BOARDS: Filled Boards
        elif user_choice == "2":
            view_boards__game_boards()


def view_boards__filled_boards() -> None:
    """Menu for viewing saved filled boards"""
    board_page: int = 0

    while True:
        # Update the saved boards lists to avoid undefined behavior
        update_board_lists()

        pages: int = max(
            1, math.ceil(len(filled_boards) / boards_per_page)
        )  # Ensure at least 1 page
        # Limit the range of `board_page` to avoid undefined behavior
        board_page: int = tools.clamp_int(0, board_page, pages - 1)
        page_range = range(
            board_page * boards_per_page,
            min((board_page * boards_per_page) + boards_per_page, len(filled_boards)),
        )

        ui_options: list[tuple[str, str]] = []

        # Checks if there are any Filled Boards to show.
        # If there aren't any, skip the unnecessary code
        if len(filled_boards) != 0:
            # Populate UI options with this page's boards
            for index in page_range:
                ui_options.append((str(index + 1), f"Board #{filled_boards[index].id}"))
            if len(filled_boards) != 0:
                # Append a newline to the last option. Separates menu options from controls
                ui_options[-1] = (ui_options[-1][0], ui_options[-1][1] + "\n")

            if board_page != 0:
                ui_options.append(("-", "Prev. Page"))
            if board_page != pages - 1:
                ui_options.append(("+", "Next Page"))
        ui_options.append(("B", "Back"))
        ui_options.append(("X", "Exit"))

        filled_boards_ui: UI = UI(
            title=f"Viewing Filled Boards ({board_page + 1}/{pages})",
        )
        filled_boards_ui_options: UI = UI(
            header=False,
            options=ui_options,
        )

        filled_boards_ui.show()
        if len(filled_boards) == 0:
            print("There are no saved Filled Boards to view!\n")
        filled_boards_ui_options.show(clr_screen=False)

        user_choice = filled_boards_ui_options.get_choice()

        # VIEW FILLED BOARDS: Exit
        if user_choice == "X":
            quit()

        # VIEW FILLED BOARDS: Back
        elif user_choice == "B":
            return

        # VIEW FILLED BOARDS: Prev. Page
        elif user_choice == "-":
            board_page -= 1

        # VIEW FILLED BOARDS: Next Page
        elif user_choice == "+":
            board_page += 1

        # VIEW FILLED BOARDS: BOARD NUM
        elif int(user_choice) - 1 in page_range:
            view_boards__show_board_ui(filled_boards[int(user_choice) - 1])


def view_boards__game_boards() -> None:
    """Menu for viewing saved game boards"""
    board_page: int = 0

    while True:
        # Update the saved boards lists to avoid undefined behavior
        update_board_lists()

        pages: int = max(
            1, math.ceil(len(game_boards) / boards_per_page)
        )  # Ensure at least 1 page
        # Limit the range of `board_page` to avoid undefined behavior
        board_page: int = tools.clamp_int(0, board_page, pages - 1)
        page_range = range(
            board_page * boards_per_page,
            min((board_page * boards_per_page) + boards_per_page, len(game_boards)),
        )

        ui_options: list[tuple[str, str]] = []

        # Checks if there are any Game Boards to show.
        # If there aren't any, skip the unnecessary code
        if len(game_boards) != 0:
            # Populate UI options with this page's boards
            for index in page_range:
                ui_options.append(
                    (
                        str(index + 1),
                        f"Board #{game_boards[index].id} (DIFF: {game_boards[index].difficulty})",
                    )
                )

            # Append a newline to the last option. Separates menu options from controls
            ui_options[-1] = (ui_options[-1][0], ui_options[-1][1] + "\n")

            if board_page != 0:
                ui_options.append(("-", "Prev. Page"))
            if board_page != pages - 1:
                ui_options.append(("+", "Next Page"))
        ui_options.append(("B", "Back"))
        ui_options.append(("X", "Exit"))

        game_boards_ui: UI = UI(
            title=f"Viewing Game Boards ({board_page + 1}/{pages})",
        )
        game_boards_ui_options: UI = UI(
            header=False,
            options=ui_options,
        )

        game_boards_ui.show()
        if len(game_boards) == 0:
            print("There are no saved Game Boards to view!\n")
        game_boards_ui_options.show(clr_screen=False)

        user_choice = game_boards_ui_options.get_choice()

        # VIEW GAME BOARDS: Exit
        if user_choice == "X":
            quit()

        # VIEW GAME BOARDS: Back
        elif user_choice == "B":
            return

        # VIEW GAME BOARDS: Prev. Page
        elif user_choice == "-":
            board_page -= 1

        # VIEW GAME BOARDS: Next Page
        elif user_choice == "+":
            board_page += 1

        # VIEW GAME BOARDS: BOARD NUM
        elif int(user_choice) - 1 in page_range:
            view_boards__show_board_ui(
                game_boards[int(user_choice) - 1], difficulty=True
            )


# CORE CONCEPT: Instance of a function with parameters
def view_boards__show_board_ui(board: Board, difficulty: bool = False) -> None:
    """Displays a single board with options to delete or go back."""
    # Display the board details, including difficulty if applicable
    show_board_ui: UI = UI(
        title=f"Viewing Board #{board.id}"
        + (f" (DIFF: {board.difficulty})" if difficulty else "")
    )
    show_board_ui.show()
    print(f"{board.format()}\n")  # Print the board's formatted representation

    # Display options for the user to delete the board, go back, or exit
    show_board_ui_options: UI = UI(
        header=False,
        options=[("D", "Delete"), ("B", "Back"), ("X", "Exit")],
    )
    show_board_ui_options.show(clr_screen=False)
    user_choice: str = show_board_ui_options.get_choice()

    # Handle user choice for the board
    # SHOW BOARD UI OPTIONS: Exit
    if user_choice == "X":
        quit()

    # SHOW BOARD UI OPTIONS: Back
    elif user_choice == "B":
        return

    # SHOW BOARD UI OPTIONS: Delete
    elif user_choice == "D":
        files.delete_board(board)  # Delete the board from storage

        # Update the saved boards lists to reflect the deletion
        update_board_lists()

        print("Deleted board!")  # Notify the user of the deletion
        time.sleep(1)


def main() -> None:
    """Where the root logic is executed"""
    # Update saved boards from disk
    update_board_lists()

    # Start the UI loop
    main_menu()


# Good practice to prevent code from running when imported...
# ...for whatever reason this might've been imported.
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nEXITING WITH KEYBOARD INTERRUPT")
        exit(0)

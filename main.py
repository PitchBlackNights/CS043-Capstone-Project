# This is a Sudoku board generator that can generate filled
# boards and starting boards at 3 different levels.
#
# It makes use of a Wave Function Collapse algorithm to
# quickly, and accurately, generate valid Sudoku boards.


from board import Board
from ui import UI
from tools import get_int, clamp_int
import files, math, time


# files.delete_path(files.save_dir)
# for cycle in range(0, 31):
#     tmp_board = Board()
#     tmp_board.generate(cycle)
#     files.save_board(tmp_board)
# for cycle in range(0, 31):
#     tmp_board = Board()
#     tmp_board.generate(cycle)
#     tmp_board.gameify(Board.Difficulty.MEDIUM)
#     files.save_board(tmp_board)


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
    """Menu for generating filled boards"""
    num_to_gen: int = get_int("Number of boards to generate: ")
    for cycle in range(num_to_gen):
        board = Board()
        board.generate(Board.last_seed + 1)

        show_board_ui: UI = UI(
            title=f"Generating Boards ({cycle + 1}/{num_to_gen}...)",
        )
        show_board_ui.show()
        print(f"Board #{board.id}\n{board.format()}\n")

        options_ui: UI = UI(
            header=False,
            options=[("1", "Save"), ("2", "Skip\n"), ("B", "Back"), ("X", "Exit")],
        )
        options_ui.show(clr_screen=False)
        user_choice: str = options_ui.get_choice()

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
            # Update the saved boards lists to avoid undefined behavior
            update_board_lists()

            print("Saved board!")
            time.sleep(1)


def generate_boards__game_boards() -> None:
    """Menu for generating game boards"""
    num_to_gen: int = get_int("Number of boards to generate: ")
    print("\nWhat difficulty level?")
    options_ui: UI = UI(
        header=False,
        options=[("1", "Easy"), ("2", "Medium"), ("3", "Hard")],
    )
    options_ui.show(clr_screen=False)
    user_difficulty: Board.Difficulty = Board.Difficulty(int(options_ui.get_choice()))

    for cycle in range(num_to_gen):
        board = Board()
        board.generate(Board.last_seed + 1)
        board.gameify(user_difficulty)

        show_board_ui: UI = UI(
            title=f"Generating Boards ({cycle + 1}/{num_to_gen}...)",
        )
        show_board_ui.show()
        print(f"Board #{board.id} (DIFF: {str(board.difficulty)})\n{board.format()}\n")

        options_ui: UI = UI(
            header=False,
            options=[("1", "Save"), ("2", "Skip\n"), ("B", "Back"), ("X", "Exit")],
        )
        options_ui.show(clr_screen=False)
        user_choice: str = options_ui.get_choice()

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
            # Update the saved boards lists to avoid undefined behavior
            update_board_lists()

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
        pages: int = math.ceil(len(filled_boards) / boards_per_page)
        # Limit the range of `board_page` (0 <= X <= `pages`) to avoid undefined behavior
        board_page: int = clamp_int(0, board_page, pages)

        ui_options: list[tuple[str, str]] = []
        page_range = range(
            board_page * boards_per_page,
            min((board_page * boards_per_page) + boards_per_page, len(filled_boards)),
        )

        # Populate UI options with this page's boards
        for index in page_range:
            ui_options.append((str(index + 1), f"Board #{filled_boards[index].id}"))
        # Append a newline to the last option. This separates them from the menu screen controls
        ui_options[-1] = (ui_options[-1][0], ui_options[-1][1] + "\n")

        if board_page != 0:
            ui_options.append(("-", "Prev. Page"))
        if board_page != pages - 1:
            ui_options.append(("+", "Next Page"))
        ui_options.append(("B", "Back"))
        ui_options.append(("X", "Exit"))

        filled_boards_ui: UI = UI(
            title=f"View Filled Boards ({board_page + 1}/{max(pages, 1)})",
            options=ui_options,
        )
        filled_boards_ui.show()
        user_choice: str = filled_boards_ui.get_choice()

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
        pages: int = math.ceil(len(filled_boards) / boards_per_page)
        # Limit the range of `board_page` (0 <= X <= `pages`) to avoid undefined behavior
        board_page: int = clamp_int(0, board_page, pages)

        ui_options: list[tuple[str, str]] = []
        page_range = range(
            board_page * boards_per_page,
            min((board_page * boards_per_page) + boards_per_page, len(game_boards)),
        )

        # Populate UI options with this page's boards
        for index in page_range:
            ui_options.append(
                (
                    str(index + 1),
                    f"Board #{game_boards[index].id} (DIFF: {game_boards[index].difficulty})",
                )
            )
        # Append a newline to the last option. This separates them from the menu screen controls
        ui_options[-1] = (ui_options[-1][0], ui_options[-1][1] + "\n")

        if board_page != 0:
            ui_options.append(("-", "Prev. Page"))
        if board_page != pages - 1:
            ui_options.append(("+", "Next Page"))
        ui_options.append(("B", "Back"))
        ui_options.append(("X", "Exit"))

        game_boards_ui: UI = UI(
            title=f"View Game Boards ({board_page + 1}/{max(pages, 1)})",
            options=ui_options,
        )
        game_boards_ui.show()
        user_choice = game_boards_ui.get_choice()

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


def view_boards__show_board_ui(board: Board, difficulty: bool = False) -> None:
    show_board_ui: UI = UI(
        title=f"Viewing Board #{board.id}"
        + (f" (DIFF: {board.difficulty})" if difficulty else "")
    )
    show_board_ui.show()
    print(f"{board.format()}\n")

    show_board_ui_options: UI = UI(
        header=False,
        options=[("D", "Delete"), ("B", "Back"), ("X", "Exit")],
    )
    show_board_ui_options.show(clr_screen=False)
    user_choice: str = show_board_ui_options.get_choice()

    # SHOW BOARD UI OPTIONS: Exit
    if user_choice == "X":
        quit()

    # SHOW BOARD UI OPTIONS: Back
    elif user_choice == "B":
        return

    # SHOW BOARD UI OPTIONS: Delete
    elif user_choice == "D":
        # Update the saved boards lists to avoid undefined behavior
        update_board_lists()

        print("Deleted board!")
        time.sleep(1)


def __main() -> None:
    """Where the root logic is executed"""
    # Update saved boards from disk
    update_board_lists()

    # Start the UI loop
    main_menu()


# Good practice to prevent code from running when imported... for whatever reason this was imported
if __name__ == "__main__":
    __main()

from board import Board
import os, pathlib


save_dir = os.path.abspath("./saved_boards")


def save_board(board: Board) -> None:
    """Write serialized board data to disk"""
    # Make sure the save directory actually exists
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
    file_path = os.path.abspath(f"{save_dir}/{board.id}.board")

    # Create the save file, and prompt user if it already exists
    try:
        open(file_path, "x").close()
    except FileExistsError:
        print(f"WARNING: Board {board.id} has already been saved!")
        if "y" in input("Overwrite it? [y/N] ").lower():
            pass
        else:
            print("Not overwriting saved board!")

    # Write serialized board data to save file
    with open(file_path, "w+") as file:
        file.write(board.serialize())


def load_saved_boards() -> list[Board]:
    """Load all saved boards on disk"""
    # Make sure the save directory actually exists
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)

    # Get list of all filenames within `save_dir`
    filenames = next(os.walk(save_dir), (None, None, []))[2]

    # Loop `filenames` and initialize + deserialize each save file
    boards: list[Board] = []
    for filename in filenames:
        if filename[-6:] == ".board":
            with open(f"{save_dir}/{filename}", "r") as file:
                tmp_board: Board = Board()
                tmp_board.deserialize(file.read())
                boards.append(tmp_board)

    return boards

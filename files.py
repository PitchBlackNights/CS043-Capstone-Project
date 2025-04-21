from board import Board
import os, pathlib, shutil
from copy import deepcopy

# Directory to save boards
save_dir: str = os.path.abspath("./saved_boards")


def delete_path(file_path: str):
    """Deletes a path on the disk"""
    abs_file_path: str = os.path.abspath(file_path)
    if (
        os.path.isfile(abs_file_path)
        or os.path.islink(abs_file_path)
        or os.path.isjunction(abs_file_path)
    ):
        os.remove(abs_file_path)
    else:
        shutil.rmtree(abs_file_path)


def save_board(board: Board, save_dir: str = save_dir) -> None:
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


def load_saved_boards(save_dir: str = save_dir) -> list[Board]:
    """Load all saved boards from disk"""
    # Make sure the save directory actually exists
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)

    # Get list of all filenames within `save_dir`
    filenames: list[str] = next(os.walk(save_dir), (None, None, []))[2]  # type: ignore

    # There are no saved boards, so return early
    if len(filenames) == 0:
        return []

    # Remove any invalid files from `filenames`
    filenames_copy: list[str] = deepcopy(filenames)
    for index, filename in enumerate(filenames):
        name: str = os.path.splitext(filename)[0]
        ext: str = os.path.splitext(filename)[1]

        is_int: bool = False
        try:
            _: int = int(name)
            is_int: bool = True
        except ValueError:
            pass

        if ext != ".board" or not is_int:
            filenames_copy.pop(index)
    filenames: list[str] = filenames_copy

    # Sort the files based on numerical value instead of characters
    for i in range(len(filenames)):
        for j in range(i + 1, len(filenames)):
            if int(filenames[i][:-6]) > int(filenames[j][:-6]):
                filenames[i], filenames[j] = filenames[j], filenames[i]

    # Loop `filenames` and initialize + deserialize each save file
    boards: list[Board] = []
    for filename in filenames:
        with open(f"{save_dir}/{filename}", "r") as file:
            tmp_board: Board = Board()
            tmp_board.deserialize(file.read())
            boards.append(tmp_board)

    return boards

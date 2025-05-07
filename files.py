from board import Board
import os, pathlib, shutil, time, serde
from copy import deepcopy
from errors import FileException, DeserializerException

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
    # Sleep for just a bit to avoid and potential weird behavior on slow systems
    time.sleep(0.100)  # 0.100 Seconds == 100 Milliseconds


def save_board(board: Board, save_dir: str = save_dir) -> None:
    """Write serialized board data to disk"""
    # Make sure the save directory actually exists
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
    file_path = os.path.abspath(f"{save_dir}/{board.id}.board")

    if not board.generated:
        raise FileException("Called `files.save_board()` on an ungenerated board!")

    # CORE CONCEPT: Instance of Try and Except
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
        file.write(serde.serialize(board))

    # Sleep for just a bit to avoid and potential weird behavior on slow systems
    time.sleep(0.100)  # 0.100 Seconds == 100 Milliseconds


def get_all_saved_board_files(
    save_dir: str = save_dir, abs_path: bool = False
) -> list[str]:
    """Returns a list of all *NAME* valid board saves, sorted by numerical value"""

    # Make sure the save directory actually exists
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)

    # Get list of all filenames within `save_dir`
    filenames: list[str] = next(os.walk(save_dir), (None, None, []))[2]  # type: ignore

    # There are no saved boards, so return early
    if len(filenames) == 0:
        return []

    # Remove any invalid files from `filenames`
    filenames_copy: list[str] = deepcopy(filenames)
    for filename in filenames:
        name: str = os.path.splitext(filename)[0]
        ext: str = os.path.splitext(filename)[1]

        if ext != ".board" or not name.isdigit():
            filenames_copy.remove(filename)
    filenames: list[str] = filenames_copy

    # Sort the files based on numerical value instead of characters
    for i in range(len(filenames)):
        for j in range(i + 1, len(filenames)):
            if int(filenames[i][:-6]) > int(filenames[j][:-6]):
                filenames[i], filenames[j] = filenames[j], filenames[i]

    # Return the Absolute Paths of the files if requested
    if abs_path:
        filenames_copy: list[str] = []
        for filename in filenames:
            filenames_copy.append(os.path.abspath(f"{save_dir}/{filename}"))
        filenames: list[str] = filenames_copy

    return filenames


def load_saved_boards(save_dir: str = save_dir) -> list[Board]:
    """Load all saved boards from disk"""
    # Make sure the save directory actually exists
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)

    # Get list of all saved board files within `save_dir`
    filenames: list[str] = get_all_saved_board_files(save_dir=save_dir)

    # Loop `filenames` and initialize + deserialize each save file
    boards: list[Board] = []
    for filename in filenames:
        delete_board: bool = False
        with open(f"{save_dir}/{filename}", "r") as file:
            try:
                tmp_board: Board = serde.deserialize(file.read())
                boards.append(tmp_board)
            except DeserializerException as err:
                print(
                    f"ERROR: A board save file is corrupted! ('{filename}')\nPROBLEMS:"
                )
                print(f"\t{'\t'.join(f'{line}\n' for line in str(err).splitlines())}")
                input("Press enter to continue...")
                print("Deleting the board save...\n")
                time.sleep(2)
                delete_board: bool = True
        if delete_board:
            try:
                delete_path(f"{save_dir}/{filename}")
            except Exception as e:
                print(f"ERROR: Failed to delete the corrupted save '{filename}': {e}")
                input("Press enter to continue...")

    return boards


def delete_board(board: Board, save_dir: str = save_dir) -> None:
    # Make sure the save directory actually exists
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)

    # Get list of all saved board files within `save_dir`
    filenames: list[str] = get_all_saved_board_files(save_dir=save_dir)

    # There are no saved boards, so raise an error.
    if len(filenames) == 0:
        raise FileException(
            "Called `files.delete_board()` when there are no boards actively saved!"
        )

    # The provided board hasn't been generated, so raise an error.
    if not board.generated:
        raise FileException("Called `files.delete_board()` on an ungenerated board!")

    # The provided board hasn't been saved, so raise an error.
    if not f"{board.id}.board" in filenames:
        raise FileException(
            "Called `files.delete_board()` on a board the hasn't been saved!"
        )

    # Required checks have passed, go ahead and delete the file (Which must exist now)
    delete_path(f"{save_dir}/{board.id}.board")

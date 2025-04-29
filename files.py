from board import Board
import os, pathlib, shutil, time
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

    # Sleep for just a bit to avoid and potential weird behavoir on systems with slow discs
    time.sleep(0.100)  # 0.100 Seconds == 100 Miliseconds


def get_all_saved_board_files(save_dir: str = save_dir) -> list[str]:
    """Returns a list of all *NAME* valid board saves, sorted by numerical value"""
    # =====================
    #     POTENTIAL BUG
    # =====================
    # A potential bug arises from the fact that all *NAME* valid board saves
    # may not be *DATA* valid.
    #
    # This means that corruptions withing a save file's data may cause bugs, or
    # otherwise undefined behavior, when deserializing the data.

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
        with open(f"{save_dir}/{filename}", "r") as file:
            tmp_board: Board = Board()
            tmp_board.deserialize(file.read())
            boards.append(tmp_board)

    return boards


def delete_board(board: Board, save_dir: str = save_dir) -> None:
    # Make sure the save directory actually exists
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)

    # Get list of all saved board files within `save_dir`
    filenames: list[str] = get_all_saved_board_files(save_dir=save_dir)

    # There are no saved boards, so raise an error.
    if len(filenames) == 0:
        raise Exception(
            "Called `files.delete_board()` when there are no boards actively saved!"
        )

    # The provided board hasn't been generated, so raise an error.
    if not board.generated:
        raise Exception(
            "Called `files.delete_board()` on a board the hasn't been generated!"
        )

    # The provided board hasn't been saved, so raise an error.
    if not f"{board.id}.board" in filenames:
        raise Exception(
            "Called `files.delete_board()` on a board the hasn't been saved!"
        )

    # Required checks have passed, so go ahead and delete the file (Which must exist now)
    delete_path(f"{save_dir}/{board.id}.board")

    # Sleep for just a bit to avoid and potential weird behavoir on systems with slow discs
    time.sleep(0.100)  # 0.100 Seconds == 100 Miliseconds

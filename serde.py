from errors import BoardException, DeserializerException
from typing import Any
from board import Board
import json


def validate_data(data: Any) -> None:
    """Validates the data passed to `Board.deserialize()`"""
    # There are no comments in this function because the code is already hard to read,
    # and adding comments into the mix will just make it even harder.

    # Validate basic data format
    if not isinstance(data, dict):
        raise DeserializerException(
            f"`data` has a type of '{type(data)}'. Expected a type of '{dict}'!"
        )
    if len(data) != 4:  # type: ignore
        raise DeserializerException(
            f"`data` has length of '{len(data)}'. Expected a length of '4'!"  # type: ignore
        )

    # Validate key types
    for key in data:  # type: ignore
        if not isinstance(key, str):
            raise DeserializerException(
                f"`data[\"{key}\"]` has a type of '{type(key)}'. Expected a type of '{str}'!"  # type: ignore
            )

    # Validate keys
    queued_exceptions: str = ""
    if "id" not in data:
        queued_exceptions += "`data` does not contain key 'id'!\n"
    if "type" not in data:
        queued_exceptions += "`data` does not contain key 'type'!\n"
    if "difficulty" not in data:
        queued_exceptions += "`data` does not contain key 'difficulty'!\n"
    if "board" not in data:
        queued_exceptions += "`data` does not contain key 'board'!\n"
    if queued_exceptions != "":
        raise DeserializerException(queued_exceptions)

    # Validate value base types
    queued_exceptions: str = ""
    if not isinstance(data["id"], str):
        queued_exceptions += f"`data[\"id\"]` has a type of '{type(data['id'])}'. Expected a type of '{str}'!\n"  # type: ignore
    if not isinstance(data["type"], int):
        queued_exceptions += f"`data[\"type\"]` has a type of '{type(data['type'])}'. Expected a type of '{int}'!\n"  # type: ignore
    if not isinstance(data["difficulty"], int):
        queued_exceptions += f"`data[\"difficulty\"]` has a type of '{type(data['difficulty'])}'. Expected a type of '{int}'!\n"  # type: ignore
    if not isinstance(data["board"], list):
        queued_exceptions += f"`data[\"board\"]` has a type of '{type(data['board'])}'. Expected a type of '{list}'!\n"  # type: ignore
    else:
        for row_index, row in enumerate(data["board"]):  # type: ignore
            if not isinstance(row, list):
                queued_exceptions += f"`data[\"board\"][{row_index}]` has a type of '{type(row)}'. Expected a type of '{list}'!\n"  # type: ignore
            else:
                for col_index, col in enumerate(row):  # type: ignore
                    if not isinstance(col, str):
                        queued_exceptions += f"`data[\"board\"][{row_index}][{col_index}]` is of type '{type(col)}'. Expected a type of '{str}'!\n"  # type: ignore
    if queued_exceptions != "":
        raise DeserializerException(queued_exceptions)

    # Validate values
    queued_exceptions: str = ""
    if not data["id"].isdigit():  # type: ignore
        queued_exceptions += f"`data[\"id\"]` has a value of '{data['id']}'. Expected a numerical string!\n"
    if data["type"] not in [0, 1, 2]:
        queued_exceptions += f"`data[\"type\"]` has a value of {data['type']}. Expected a value from [1, 2]!\n"  # Value of '0' means it's ungenerated, which we check for later
    if data["difficulty"] not in [0, 1, 2, 3]:
        queued_exceptions += f"`data[\"difficulty\"]` has a value of {data['difficulty']}. Expected a value from [0, 1, 2, 3]!\n"
    if len(data["board"]) != 9:  # type: ignore
        queued_exceptions += f"`data[\"board\"]` has a length of {len(data['board'])}. Expected a length of 9!\n"  # type: ignore
    else:
        for row_index, row in enumerate(data["board"]):  # type: ignore
            if len(row) != 9:  # type: ignore
                queued_exceptions += f'`data["board"][{row_index}]` has a length of {len(row)}. Expected a length of 9!\n'  # type: ignore
            else:
                for col_index, col in enumerate(row):  # type: ignore
                    if col not in [" ", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        queued_exceptions += f"`data[\"board\"][{row_index}][{col_index}]` has a value of '{col}'. Expected a numerical string, or ' '!\n"  # type: ignore
    if data["type"] == 0:
        queued_exceptions += f"This board has not been generated!\n"
    if queued_exceptions != "":
        raise DeserializerException(queued_exceptions)


def deserialize(data_str: str) -> Board:
    """Deserializes a board's data from a JSON string."""
    # Parse the JSON string into a Python dictionary
    data = json.loads(data_str)

    # Validate the parsed data to ensure it conforms to the expected structure
    validate_data(data)

    # Create a new Board instance and populate its attributes
    board: Board = Board()
    board.id = data["id"]  # Set the board's unique ID
    Board.last_seed = max(int(board.id), Board.last_seed)  # Update the last seed
    board.type = Board.Type(data["type"])  # Set the board type
    board.difficulty = Board.Difficulty(data["difficulty"])  # Set the difficulty level
    board.board = data["board"]  # Set the board's cell values
    board.generated = True  # Mark the board as generated

    return board  # Return the deserialized Board object


def serialize(board: Board) -> str:
    """Serializes a board's data into a JSON string."""
    # Ensure the board has been generated before serializing
    if not board.generated:
        raise BoardException("Called `Board.serialize()` on an ungenerated board!")

    # Create a dictionary representation of the board
    data: dict[str, str | int | list[list[str]]] = {
        "id": board.id,  # Board's unique ID
        "type": int(board.type),  # Board type as an integer
        "difficulty": int(board.difficulty),  # Difficulty level as an integer
        "board": board.board,  # Board's cell values
    }

    # Convert the dictionary to a JSON string and return it
    return json.dumps(data)

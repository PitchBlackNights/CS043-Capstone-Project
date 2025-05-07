from enum import IntEnum
from cell import Cell
from copy import deepcopy
from rand_man import Rand
from errors import BoardException
import random


class Board:
    last_seed: int = 0  # Tracks the last seed used for board generation

    class Type(IntEnum):
        """Enum for board types."""

        NONE = 0  # No type assigned
        FULL = 1  # Fully filled board
        GAME = 2  # Game board with some cells removed

    class Difficulty(IntEnum):
        """Enum for difficulty levels."""

        NONE = 0  # No difficulty assigned
        EASY = 1  # Easy difficulty
        MEDIUM = 2  # Medium difficulty
        HARD = 3  # Hard difficulty

        def __str__(self) -> str:
            """Returns the string representation of the difficulty."""
            text = ""
            if self.value == 1:
                text = "Easy"
            elif self.value == 2:
                text = "Medium"
            elif self.value == 3:
                text = "Hard"

            return text

    def __eq__(self, value: object) -> bool:
        """Checks if two boards are equal."""
        if type(value) != Board:  # Ensure the other object is a Board
            return False

        # Compare all relevant attributes for equality
        return (
            (self.id == value.id)
            and (self.type == value.type)
            and (self.difficulty == value.difficulty)
            and (self.board == value.board)
            and (self.generated == value.generated)
        )

    def __init__(self) -> None:
        """Initializes a new board with default values."""
        self.id: str = ""  # Unique identifier for the board
        self.type: Board.Type = Board.Type.NONE  # Board type
        self.difficulty: Board.Difficulty = Board.Difficulty.NONE  # Difficulty level
        # CORE CONCEPT: Instance of a 2D list
        self.board: list[list[str]] = [
            [" " for _ in range(9)] for _ in range(9)
        ]  # Public board representation
        # CORE CONCEPT: Instance of a hidden attribute
        self.__board: list[list[Cell]] = [
            [Cell() for _ in range(9)] for _ in range(9)
        ]  # Internal board representation
        self.generated: bool = False  # Flag indicating if the board has been generated

    def gameify(self, difficulty: Difficulty) -> None:
        """Convert a full board into a game board by removing cells."""
        if not self.generated:
            raise BoardException(
                "Called `Board.gameify()` on an ungenerated board!"
            )  # Ensure the board is generated

        if not self.difficulty == Board.Difficulty.NONE:
            raise BoardException(
                "Called `Board.gameify()` on an already gameified board!"  # Ensure the board is not already gameified
            )

        self.difficulty: Board.Difficulty = difficulty  # Set the difficulty level
        self.type: Board.Type = Board.Type.GAME  # Set the board type to GAME

        # Determine the number of cells to remove based on difficulty
        if difficulty == Board.Difficulty.MEDIUM:
            num_to_remove: int = 37
        elif difficulty == Board.Difficulty.HARD:
            num_to_remove: int = 46
        else:  # Equivalent to `difficulty == Board.Difficulty.EASY`
            num_to_remove: int = 28

        # Gather a list of all cell coordinates
        cells: list[tuple[int, int]] = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                # CORE CONCEPT: Instance of a `tuple` or `list` with methods used on them
                cells.append((x, y))
        removed_cells: list[tuple[int, int]] = random.sample(
            cells, num_to_remove
        )  # Randomly select cells to remove

        # Remove the selected cells from the board
        for x, y in removed_cells:
            self.board[y][x] = " "  # Clear the cell

    def format(self) -> str:
        """Returns the stored Sudoku board as a formatted string table."""
        # Define the table components
        head: str = "╭───────┬───────┬───────╮"
        mid: str = "├───────┼───────┼───────┤"
        foot: str = "╰───────┴───────┴───────╯"
        sep: str = "│"
        text: str = ""

        # Construct the formatted table
        text += f"{head}\n"
        for table_row in range(3):  # Iterate over the 3x3 grid of blocks
            for inner_row in range(3):  # Iterate over rows within each block
                for table_column in range(3):  # Iterate over columns within each block
                    text += f"{sep} "
                    for inner_column in range(
                        3
                    ):  # Iterate over cells within each block
                        text += f"{self.board[(table_row * 3) + inner_row][(table_column * 3) + inner_column]} "
                text += f"{sep}\n"
            if (
                table_row != 2
            ):  # Add a separator between blocks, except after the last block
                text += f"{mid}\n"
        text += f"{foot}"  # Add the table footer

        return text  # Return the formatted board as a string

    def generate(self, seed: int) -> None:
        """Generate a board with the provided seed."""
        if self.generated:
            # Prevent generating a board that has already been generated
            raise BoardException(
                "Called `Board.generate()` on an already generated board!"
            )

        # Set the random seed for board generation
        Rand.set_seed(seed)  # type: ignore
        self.id: str = str(seed)  # Assign the seed as the board's unique ID
        if (
            seed > Board.last_seed
        ):  # Update the last seed if the current seed is greater
            Board.last_seed: int = seed

        while True:
            # Check for contradictions in the board
            if self.__has_contradiction():
                self.__reset()  # Reset the board if contradictions are found

            # Get the lowest entropy value among all cells
            lowest_entropy: int = self.__get_lowest_entropy()

            if lowest_entropy == 10:
                # If all cells are resolved (entropy is 0), the board is fully generated
                self.generated = True
                break

            # Find all cells with the lowest entropy
            coords: list[tuple[int, int]] = []
            for y in range(len(self.__board)):
                for x in range(len(self.__board[y])):
                    if self.__board[y][x].get_entropy() == lowest_entropy:
                        # CORE CONCEPT: Instance of packing
                        coords.append((x, y))

            # Randomly select one of the cells with the lowest entropy
            # `coords` is guaranteed to be populated because the board is not solved
            selected_cell_index: int = Rand.random() % len(coords)  # type: ignore
            # CORE CONCEPT: Instance of unpacking
            x, y = coords[selected_cell_index]

            # Collapse the selected cell to a single value
            self.__board[y][x].collapse()
            value = self.__board[y][x].get_value()

            # Propagate the collapsed value to other cells

            # Update the row and column to remove the collapsed value as a choice
            for index in range(9):
                self.__board[y][index].remove_choice(value)  # type: ignore
                self.__board[index][x].remove_choice(value)  # type: ignore

            # Update the 3x3 box to remove the collapsed value as a choice
            box_x: int = x // 3
            box_y: int = y // 3
            for y in range(box_y * 3, (box_y * 3) + 3):
                for x in range(box_x * 3, (box_x * 3) + 3):
                    self.__board[y][x].remove_choice(value)  # type: ignore

        # Copy the resolved values from the internal board to the public board
        for y in range(9):
            for x in range(9):
                self.board[y][x] = str(self.__board[y][x].get_value())

        # Mark the board as fully filled
        self.type = Board.Type.FULL

    def __get_lowest_entropy(self) -> int:
        """Returns the lowest, non-zero, cell entropy."""
        lowest_entropy: int = 10  # Start with the maximum possible entropy

        # Iterate through all cells to find the lowest entropy
        for y in range(len(self.__board)):
            for x in range(len(self.__board[y])):
                entropy: int = self.__board[y][x].get_entropy()

                # Update the lowest entropy if a smaller non-zero value is found
                if (entropy < lowest_entropy) and (entropy > 0):
                    lowest_entropy = entropy

        return lowest_entropy

    def __has_contradiction(self) -> bool:
        """Checks if any cell has a contradiction."""
        # Iterate through all cells to check for contradictions
        for y in range(len(self.__board)):
            for x in range(len(self.__board[y])):
                if self.__board[y][x].has_contradiction():
                    return True  # Return True if a contradiction is found

        return False  # Return False if no contradictions are found

    def __reset(self) -> None:
        """Resets the board to its initial state."""
        self.__board: list[list[Cell]] = []  # Clear the internal board

        # Populate the internal board with a 9x9 grid of new cells
        row: list[Cell] = []
        for _ in range(9):
            row.append(Cell())
        for _ in range(9):
            self.__board.append(deepcopy(row))

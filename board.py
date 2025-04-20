from enum import IntEnum
from cell import Cell
from copy import deepcopy
from rand_man import Rand
import random, json


class Board:
    last_seed: int = 0

    class Type(IntEnum):
        NONE = 0
        FULL = 1
        GAME = 2

    class Difficulty(IntEnum):
        NONE = 0
        EASY = 1
        MEDIUM = 2
        HARD = 3

        def __str__(self) -> str:
            text = ""
            if self.value == 1:
                text = "Easy"
            elif self.value == 2:
                text = "Medium"
            elif self.value == 3:
                text = "Hard"

            return text

    def __init__(self) -> None:
        # Initialize the board with default values
        self.id: str = ""
        self.type: Board.Type = Board.Type.NONE
        self.difficulty: Board.Difficulty = Board.Difficulty.NONE
        self.board: list[list[str]] = []
        self.__board: list[list[Cell]] = []
        self.generated: bool = False

        # Populate `self.board` with a 2D list with 9x9 dimensions
        row_norm: list[str] = []
        for _ in range(9):
            row_norm.append(" ")
        for _ in range(9):
            self.board.append(deepcopy(row_norm))

        # Populate `self.__board` with a 2D list with 9x9 dimensions
        row_hide: list[Cell] = []
        for _ in range(9):
            row_hide.append(Cell())
        for _ in range(9):
            self.__board.append(deepcopy(row_hide))

    def gameify(self, difficulty: Difficulty) -> None:
        """Convert a full board into a game board by removing cells"""
        if not self.generated:
            raise Exception("Called `Board.gameify()` on an ungenerated board!")

        if not self.difficulty == Board.Difficulty.NONE:
            raise Exception("Called `Board.gameify()` on an already gameified board!")

        self.difficulty: Board.Difficulty = difficulty
        self.type: Board.Type = Board.Type.GAME

        # Only remove a certain number of cells, based on the difficulty
        if difficulty == Board.Difficulty.MEDIUM:
            num_to_remove: int = 37
        elif difficulty == Board.Difficulty.HARD:
            num_to_remove: int = 46
        else:  # Equivalent to `difficulty == Board.Difficulty.EASY`
            num_to_remove: int = 28

        # Gather list of cell coordinates for `random.sample()`
        cells: list[tuple[int, int]] = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                cells.append((x, y))
        removed_cells = random.sample(cells, num_to_remove)

        # Remove cells from `self.board`
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if (x, y) in removed_cells:
                    self.board[y][x] = " "

    def format(self) -> str:
        """Returns the stored Sudoku board as a formatted string table"""
        head: str = "╭───────┬───────┬───────╮"
        mid: str = "├───────┼───────┼───────┤"
        foot: str = "╰───────┴───────┴───────╯"
        sep: str = "│"
        text: str = ""

        text += f"{head}\n"
        for table_row in range(3):
            for inner_row in range(3):
                for table_column in range(3):
                    text += f"{sep} "
                    for inner_column in range(3):
                        text += f"{self.board[(table_row * 3) + inner_row][(table_column * 3) + inner_column]} "
                text += f"{sep}\n"
            if table_row != 2:
                text += f"{mid}\n"
        text += f"{foot}"

        return text

    def serialize(
        self,
    ) -> str:
        """Serialize the board data into a JSON string"""
        data: dict[str, str | int | list[list[str]]] = {
            "id": self.id,
            "type": int(self.type),
            "difficulty": int(self.difficulty),
            "board": self.board,
        }
        return json.dumps(data)

    def deserialize(
        self,
        data_str: str,
    ) -> None:
        """Deserialize the board data from a JSON string"""
        data = json.loads(data_str)
        self.id: str = data["id"]
        if int(data["id"]) > Board.last_seed:
            Board.last_seed: int = int(data["id"])
        self.type: Board.Type = Board.Type(data["type"])
        self.difficulty: Board.Difficulty = Board.Difficulty(data["difficulty"])
        self.board: list[list[str]] = data["board"]
        self.generated: bool = True

    def generate(self, seed: int) -> None:
        """Generate a board with the provided seed"""
        if self.generated:
            raise Exception("Called `Board.generate()` on an already generated board!")

        Rand.set_seed(seed)  # type: ignore
        self.id: str = str(seed)
        if seed > Board.last_seed:
            Board.last_seed: int = seed

        while True:
            if self.__has_contradiction():
                self.__reset()

            lowest_entropy: int = self.__get_lowest_entropy()

            if lowest_entropy == 10:
                # There are no contradictions and all entropies are 0
                self.generated = True
                break

            # List of cells with lowest entropy
            coords: list[tuple[int, int]] = []

            for y in range(len(self.__board)):
                for x in range(len(self.__board[y])):
                    if self.__board[y][x].get_entropy() == lowest_entropy:
                        coords.append((x, y))

            # Select random cell out of the cells with the lowest entropy
            # Coords is guaranteed to be populated because the board is not currently solved
            selected_cell_index: int = Rand.random() % len(coords)  # type: ignore
            x, y = coords[selected_cell_index]

            # Collapse cell
            self.__board[y][x].collapse()
            value = self.__board[y][x].get_value()

            # Propogate cell information

            # Update row and column choices
            for index in range(9):
                self.__board[y][index].remove_choice(value)  # type: ignore
                self.__board[index][x].remove_choice(value)  # type: ignore

            # Update box choices
            box_x: int = x // 3
            box_y: int = y // 3

            for y in range(box_y * 3, (box_y * 3) + 3):
                for x in range(box_x * 3, (box_x * 3) + 3):
                    self.__board[y][x].remove_choice(value)  # type: ignore

        # Copy cell values from `self.__board` to `self.board`
        for y in range(9):
            for x in range(9):
                self.board[y][x] = str(self.__board[y][x].get_value())

        self.type = Board.Type.FULL

    def __get_lowest_entropy(self) -> int:
        """Returns the lowest, non-zero, cell entropy"""
        lowest_entropy: int = 10

        for y in range(len(self.__board)):
            for x in range(len(self.__board[y])):
                entropy: int = self.__board[y][x].get_entropy()

                if (entropy < lowest_entropy) and (entropy > 0):
                    lowest_entropy = entropy

        return lowest_entropy

    def __has_contradiction(self) -> bool:
        """Does any cell have a contradiction?"""
        for y in range(len(self.__board)):
            for x in range(len(self.__board[y])):
                if self.__board[y][x].has_contradiction():
                    return True

        return False

    def __reset(self) -> None:
        """Resets the board"""
        self.__board: list[list[Cell]] = []

        # Populate `self.__board` with a 2D list with 9x9 dimensions
        row: list[Cell] = []
        for _ in range(9):
            row.append(Cell())
        for _ in range(9):
            self.__board.append(deepcopy(row))

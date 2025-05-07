from typing import Optional
from rand_man import Rand
from copy import deepcopy
from errors import CellException


class Cell:
    def __init__(self):
        # Initialize cell with all possible values and no set value
        self.options: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.value: Optional[int] = None

    def get_value(self) -> Optional[int]:
        """Returns the cell's value"""
        return self.value

    def get_entropy(self) -> int:
        """Returns the cell's entropy"""
        return len(self.options)

    def is_collapsed(self) -> bool:
        """Is the cell collapsed?"""
        return type(self.value) is int

    def has_contradiction(self) -> bool:
        """Is the cell not collapsed and has 0 entropy?"""
        return (not self.is_collapsed()) and (self.get_entropy() == 0)

    def remove_choice(self, val: int) -> None:
        """Removes `val` from cell's `options`"""
        for index in range(len(self.options)):
            if self.options[index] == val:
                self.options.pop(index)
                break

    def collapse(self) -> None:
        """Collapses the cell into a random, valid, option"""
        if (len(self.options) == 0) and (self.value == None):
            raise CellException("Cell has no valid states, the universe will explode!")

        choice_index: int = Rand.random() % len(self.options)  # type: ignore
        choice = deepcopy(self.options[choice_index])
        self.options = []

        self.value = choice

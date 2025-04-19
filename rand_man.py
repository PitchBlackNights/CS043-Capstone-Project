import random, sys
from typing import Any


class Rand:
    state: tuple[Any, ...] = ()
    seed: int = 0
    local_random: random.Random = random.Random(seed)

    def set_seed(val: int) -> None:  # type: ignore
        Rand.seed: int = val
        Rand.local_random: random.Random = random.Random(Rand.seed)

    def set_state(val: tuple[Any, ...]) -> None:  # type: ignore
        Rand.state: tuple[Any, ...] = val
        Rand.local_random.setstate(Rand.state)

    def get_state() -> tuple[Any, ...]:  # type: ignore
        return Rand.local_random.getstate()

    def random() -> int:  # type: ignore
        return Rand.local_random.randint(0, sys.maxsize)

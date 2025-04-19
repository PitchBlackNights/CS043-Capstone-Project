import random, sys

class Rand:
    seed: int = 0
    local_random: random.Random = random.Random(seed)

    def set_seed(val: int) -> None: # type: ignore
        Rand.seed: int = val
        Rand.local_random: random.Random = random.Random(Rand.seed)

    def random() -> int: # type: ignore
        return Rand.local_random.randint(0, sys.maxsize)

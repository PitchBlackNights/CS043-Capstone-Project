import random, sys


class Rand:
    # Static class for managing random number generation with a seed
    seed: int = 0
    local_random: random.Random = random.Random(seed)

    def set_seed(val: int) -> None:  # type: ignore
        """Set the seed for the random number generator"""
        Rand.seed: int = val
        Rand.local_random: random.Random = random.Random(Rand.seed)

    def random() -> int:  # type: ignore
        """Generate a random integer"""
        return Rand.local_random.randint(0, sys.maxsize)

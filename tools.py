import time


def clamp_int(min_num: int, num: int, max_num: int) -> int:
    """Limits the range of `num` to between `min_num` and `max_num` (Inclusive)"""
    return max(min(max_num, num), min_num)


def get_int(text: str) -> int:
    """Gets an valid integer from the user"""
    while True:
        try:
            user_int: int = int(input(text))
            return user_int
        except ValueError:
            print("That's not a number!")
            time.sleep(1)
            # Sets cursor 2 lines up, then erases to the end of the screen
            print("\x1b[2F\x1b[0J", end="")

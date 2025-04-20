import time


def clear_screen() -> None:
    print("\x1b[2J\x1b[H", end="")


class UI:
    def __init__(
        self, title: str = "", header: bool = True, options: list[tuple[str, str]] = []
    ):
        self.header_text: str = (
            f"SUDOKU BOARD GENERATOR  v0.1\n{title}\n============================="
        )
        self.header: bool = header
        self.options: list[tuple[str, str]] = options

    def show(self, clr_screen=True):
        """Prints out this UI interface"""
        text: str = ""
        if self.header:
            text += f"{self.header_text}{"\n" if len(self.options) != 0 else ""}"
        for option_key, option_text in self.options:
            text += f"[{option_key}] {option_text}\n"

        if clr_screen:
            clear_screen()
        print(text)

    def get_choice(self) -> str:
        valid_keys: list[str] = [key for key, _ in self.options]
        while True:
            user_choice: str = input("Option: ")
            if not user_choice in valid_keys:
                print(f"ERROR: '{user_choice}' is not a valid option!")
                time.sleep(1)
                # Sets cursor 2 lines up, then erases to the end of the screen
                print("\x1b[2F\x1b[0J", end="")
            else:
                return user_choice

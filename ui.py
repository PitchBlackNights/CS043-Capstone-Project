import time


VERSION: str = "0.2-BETA"


def clear_screen() -> None:
    """Clear the terminal screen"""
    print("\x1b[2J\x1b[H", end="")


class UI:
    def __init__(
        self, title: str = "", header: bool = True, options: list[tuple[str, str]] = []
    ):
        # Initialize the UI with a title, header, and options
        self.header_text: str = (
            f"SUDOKU BOARD GENERATOR  v{VERSION}\n{title}\n"
        )
        self.header_text += "=" * (max(len(f"SUDOKU BOARD GENERATOR  v{VERSION}"), len(title)) + 1)

        self.header: bool = header
        self.options: list[tuple[str, str]] = options

    def show(self, clr_screen: bool = True):
        """Display the UI on the screen"""
        text: str = ""
        if self.header:
            text += self.header_text + ("\n\n" if len(self.options) != 0 else "")
        for option_key, option_text in self.options:
            text += f"[{option_key}] {option_text}\n"

        if clr_screen:
            clear_screen()
        print(text)

    def get_choice(self) -> str:
        """Get a valid choice from the user"""
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

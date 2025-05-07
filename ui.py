import time


VERSION: str = "0.3.1-BETA"


def clear_screen() -> None:
    """Clears the terminal screen"""
    print("\x1b[2J\x1b[H", end="")


class UI:
    def __init__(
        self, title: str = "", header: bool = True, options: list[tuple[str, str]] = []
    ):
        # Initialize the UI with a title, header, and options
        self.header_text: str = f"SUDOKU BOARD GENERATOR  v{VERSION}\n{title}\n"
        self.header_text += "=" * (
            max(len(f"SUDOKU BOARD GENERATOR  v{VERSION}"), len(title)) + 1
        )

        self.header: bool = header
        self.options: list[tuple[str, str]] = options

    def show(self, clr_screen: bool = True):
        """Display the UI on the screen."""
        text: str = ""  # Initialize the text to display
        if self.header:  # If the header is enabled, add it to the text
            text += self.header_text + ("\n\n" if len(self.options) != 0 else "\n")
        for option_key, option_text in self.options:  # Add each option to the text
            text += f"[{option_key}] {option_text}\n"

        if clr_screen:  # Clear the screen if the flag is set
            clear_screen()
        print(text)  # Print the constructed UI text

    def get_choice(self) -> str:
        """Get a valid choice from the user."""
        valid_keys: list[str] = [key for key, _ in self.options]  # Extract valid keys
        while True:
            user_choice: str = input("Option: ")  # Prompt the user for input
            if not user_choice in valid_keys:  # Check if the input is invalid
                print(f"ERROR: '{user_choice}' is not a valid option!")  # Show error
                time.sleep(2)  # Pause briefly to let the user read the error
                # Move the cursor up 2 lines and clear the screen from that point
                print("\x1b[2F\x1b[0J", end="")
            else:
                return user_choice  # Return the valid user choice

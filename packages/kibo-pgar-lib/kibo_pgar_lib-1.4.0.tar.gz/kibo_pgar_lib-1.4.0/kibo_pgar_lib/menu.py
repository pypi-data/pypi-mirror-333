"""Module for the Menu class"""

# Standard Modules
import time

# Internal Modules
from kibo_pgar_lib.ansi_colors import AnsiFontColors
from kibo_pgar_lib.input_data import InputData
from kibo_pgar_lib.known_problems import KnownProblems
from kibo_pgar_lib.pretty_strings import PrettyStrings


class Menu:
    """
    This class creates a menu with multiple entries, assuming that zero is always the exit option.
    The class also contains some methods that may be useful for visualizing the menu.
    """

    _NEW_LINE = "\n"
    _EXIT_ENTRY = "0. Exit"
    _INSERT_REQUEST = "> "
    _NEGATIVE_MILLIS_ERROR = "Impossible to wait for a negative time."

    def __init__(
        self,
        title: str,
        entries: list[str],
        use_exit_entry: bool,
        centred_title: bool,
    ) -> None:
        """Creates a Menu object specifying some configuration parameters.

        Params
        ------
        - `title` -> The title of the menu.
        - `entries` -> The entries, options, of the menu.
        - `use_exit_entry` -> If you want the exit entry or not.
        - `centred_title` -> If you want the title to be centred or not.
        """
        self._title = title
        self._entries = entries
        self._use_exit_entry = use_exit_entry
        self._frame_length = self._calculate_frame_length()
        self._centred_title = centred_title
        self._use_vertical_frame = False

    @property
    def use_vertical_frame(self) -> bool:
        """Gets the value of the use_vertical_frame attribute.

        Returns
        -------
        A bool representing the attribute value.
        """
        return self._use_vertical_frame

    @use_vertical_frame.setter
    def use_vertical_frame(self, value: bool) -> None:
        """Sets the value of the use_vertical_frame attribute.

        Params
        ------
        - `value` -> The value to set the attribute to.
        """
        self._use_vertical_frame = value

    def _calculate_frame_length(self) -> int:
        """Calculates the frame length by measuring the length of the title and of all the entries
        of the menu, accounting for their number and the ". " string before the actual entry.

        Returns
        -------
        An integer representing the length of the frame.
        """
        frame_length = len(self._title)

        for i, entry in enumerate(self._entries):
            # The +2 is for the dot and space (es. "3. ")
            entry_length = len(entry) + KnownProblems.count_integer_digits(i + 1) + 2

            frame_length = max(frame_length, entry_length)

        return frame_length + 10  # Adding a bit of extra space

    def _print_menu(self) -> None:
        """Prints the menu, the framed title, followed by all the entries."""
        menu: list[str] = [
            PrettyStrings.frame(
                self._title,
                self._frame_length,
                self._centred_title,
                self._use_vertical_frame,
            )
        ]

        for i, entry in enumerate(self._entries):
            menu.append("".join([str(i + 1), ". ", entry, self._NEW_LINE]))

        if self._use_exit_entry:
            menu.append(PrettyStrings.isolated_line(self._EXIT_ENTRY))

        print("".join(menu))

    def choose(self) -> int:
        """Prints the menu and lets the user choose an option from it.

        Returns
        -------
        An integer representing the choice of the user.
        """
        self._print_menu()

        if self._use_exit_entry:
            min_value = 0
        else:
            min_value = 1

        return InputData.read_integer_between(
            self._INSERT_REQUEST, min_value, len(self._entries)
        )

    @staticmethod
    def clear_console() -> None:
        """Clears the console screen."""
        print(AnsiFontColors.CLEAR)

    @staticmethod
    def wait(milliseconds: int) -> None:
        """Stops the program for a certain amount of milliseconds.

        Params
        ------
        - `milliseconds` -> The number of milliseconds to stop the program.

        Raises
        ------
        - `ValueError` -> When the milliseconds are negative.
        """
        if milliseconds < 0:
            raise ValueError(Menu._NEGATIVE_MILLIS_ERROR)

        time.sleep(milliseconds / 1000)

    @staticmethod
    def loading_message(message: str) -> None:
        """Prints a certain message simulating a loading by adding dots to it slowly.

        Params
        ------
        - `message` -> The message to print.
        """

        print(message, end="", flush=True)
        for _ in range(3):
            Menu.wait(1000)
            print(".", end="", flush=True)

        Menu.wait(1000)
        Menu.clear_console()

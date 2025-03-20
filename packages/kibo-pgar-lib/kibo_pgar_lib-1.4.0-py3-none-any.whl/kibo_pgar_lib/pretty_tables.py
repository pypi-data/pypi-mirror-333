"""Module used for pretty printing a table to the terminal.

This module provides:
- The enum Alignment.
- The class CommandLineTable.
"""

# Standard Modules
from enum import IntEnum
from typing import Any

# Internal Modules
from kibo_pgar_lib.ansi_colors import AnsiFontColors, AnsiFontWeights
from kibo_pgar_lib.pretty_strings import PrettyStrings


class Alignment(IntEnum):
    """Enum to specify the table cells alignment."""

    LEFT: int = -1
    CENTER: int = 0
    RIGHT: int = 1


class CommandLineTable:
    """Class to handle the visualization of a table in a terminal."""

    _RED_ERROR: str = PrettyStrings.prettify(
        "Error!", AnsiFontColors.RED, AnsiFontWeights.BOLD
    )
    _UNKNOWN_ALIGNMENT_EXCEPTION: str = "Impossible to set alignment, value unknown."
    _SET_HEADERS_EXCEPTION: str = "The headers can only be a list of strings."
    _SET_ROWS_EXCEPTION: str = (
        "All the rows must be lists of the same length as of the headers."
    )

    _HORIZONTAL_SEPARATOR: str = "-"
    _VERTICAL_SEPARATOR: str = "|"
    _JOIN_SEPARATOR: list[str] = [" ", "+"]

    def __init__(self) -> None:
        """Creates a new instance of this class with default settings.

        The defaults settings, and so the attributes, are:
        - `show_vlines` -> If show or not the vertical lines of the table, default: False.
        - `cell_alignment` -> The cell alignment given from the Alignment enum, default: LEFT.
        - `headers` -> The list of headers, default: empty list
        - `rows` -> The rows of the table, default: empty bi-dimensional list
        """
        self.show_vlines: bool = False
        self.cell_alignment: Alignment = Alignment.LEFT
        self.headers: list[str] = []
        self.rows: list[list[str]] = []

    # This complex systems of mirrors and levers is because I'm a lazy bum and I didn't want to
    # write all the getters and setters. I love python :)
    def __getattr__(self, name: str) -> Any:
        return self.__dict__[f"_{name}"]

    def __setattr__(self, name: str, value: Any) -> None:
        match name:
            case "show_vlines":
                value = bool(value)

            case "cell_alignment":
                value = int(value)

                allowed_values: list[int] = list(map(int, Alignment))
                if value not in allowed_values:
                    raise ValueError(
                        " ".join(
                            [
                                CommandLineTable._RED_ERROR,
                                CommandLineTable._UNKNOWN_ALIGNMENT_EXCEPTION,
                            ]
                        )
                    )

            case "headers":
                if not isinstance(value, list):
                    raise ValueError(
                        " ".join(
                            [
                                CommandLineTable._RED_ERROR,
                                CommandLineTable._SET_HEADERS_EXCEPTION,
                            ]
                        )
                    )

                value = list(map(str, value))

            case "rows":
                if not (
                    isinstance(value, list)
                    and all(
                        isinstance(row, list) and len(row) == len(self.headers)
                        for row in value
                    )
                ):
                    raise ValueError(
                        " ".join(
                            [
                                CommandLineTable._RED_ERROR,
                                CommandLineTable._SET_ROWS_EXCEPTION,
                            ]
                        )
                    )

                value = [[str(val) for val in row] for row in value]

        self.__dict__[f"_{name}"] = value

    def add_headers(self, headers: list[Any]) -> None:
        """Adds the given headers, converted to string, to this table headers. Since this operation
        increases the table size a number of empty strings equal to that of the given headers will
        be added to all the rows of this table.

        Params
        ------
        - `headers` -> The headers to add to this table headers.
        """
        headers = list(map(str, headers))
        self.headers.extend(headers)

        for row in self.rows:
            row.extend([""] * len(headers))

    def add_rows(self, rows: list[list[Any]]) -> None:
        """Adds the given rows, converted to string, to this table rows. Remember that the length
        of every row must be equal to that of the headers!

        Params
        ------
        - `rows` -> The rows to add to this table rows.

        Raises
        ------
        - `ValueError` -> If the rows are not all of a length equal to that of the headers of this
        table.
        """
        rows = [[str(value) for value in row] for row in rows]

        if not all(len(row) == len(self.headers) for row in rows):
            raise ValueError(
                " ".join(
                    [
                        CommandLineTable._RED_ERROR,
                        CommandLineTable._SET_ROWS_EXCEPTION,
                    ]
                )
            )

        self.rows.extend(rows)

    def fill_holes(self, fillings: list[list[Any]]):
        """Will fill all the holes left by a previous add_headers(...) call. Be aware that, as one
        can expect, if the dimension of the fillings is smaller than that of the holes, some will
        remain, on the other hand, if it's bigger not all fillings will be used.

        Lets look at an example. I'll use X and O for demonstration purposes, where X is a occupied
        space and O represents empty, look at this table:

        |X X X O O|

        |X X X O O|

        |X X X O O|

        If the given fillings table is like this:

        |X X|

        |X X|

        Or like this:

        |X|

        |X|

        |X|

        The result table will be something like:

        |X X X X X |

        |X X X X X |

        |X X X O O|

        In the first case, while in the second one like this:

        |X X X X O|

        |X X X X O|

        |X X X X O|

        Params
        ------
        - `fillings` -> The bi-dimensional list with the fillings for this table
        """
        fillings = [[str(value) for value in row] for row in fillings]

        fill_i: int = 0
        for i, row in enumerate(self.rows):
            fill_j: int = 0
            filled: bool = False
            for j, cell in enumerate(row):
                if (
                    fill_i < len(fillings)
                    and fill_j < len(fillings[fill_i])
                    and not cell
                ):
                    self.rows[i][j] = fillings[fill_i][fill_j]
                    filled = True
                    fill_j += 1

            fill_i += 1 if filled else 0

    def _get_max_width_per_column(self) -> list[int]:
        """Calculates the maximum width needed to print each column. It will add 2 spaces if the
        alignment is set to center, 1 otherwise.

        Returns
        -------
        A list of integers representing the widths of each column.
        """
        widths: list[int] = [0] * len(self.headers)
        table: list[list[str]] = [self.headers]
        table.extend(self.rows)

        for row in table:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(cell))

        return list(
            map(
                lambda x: x + (2 if self.cell_alignment == Alignment.CENTER else 1),
                widths,
            )
        )

    def _build_hframe(self, widths: list[int]) -> str:
        """Uses the currently set options to build the horizontal frame that will be used to
        separate each row.

        Params
        ------
        - `widths` -> A list of the widths of each column.

        Returns
        -------
        A string containing the horizontal frame.
        """
        frame_str_builder: list[str] = []

        for i, width in enumerate(widths):
            frame_piece_str_builder: list[str] = []
            if i == 0 and self.show_vlines:
                frame_piece_str_builder.append(CommandLineTable._JOIN_SEPARATOR[1])

            frame_piece_str_builder.append(
                PrettyStrings.repeat_char(CommandLineTable._HORIZONTAL_SEPARATOR, width)
            )

            frame_piece_str_builder.append(
                CommandLineTable._JOIN_SEPARATOR[int(self.show_vlines)]
            )

            frame_str_builder.append("".join(frame_piece_str_builder))

        return "".join(frame_str_builder)

    def __str__(self) -> str:
        table_str_builder: list[str] = []
        widths: list[int] = self._get_max_width_per_column()

        table: list[list[str]] = [self.headers]
        table.extend(self.rows)

        horizontal_frame: str = self._build_hframe(widths)

        for row in table:
            table_str_builder.append(horizontal_frame)

            row_str_builder: list[str] = []
            for i, cell in enumerate(row):
                if i == 0 and self.show_vlines:
                    row_str_builder.append(self._VERTICAL_SEPARATOR)

                if self.cell_alignment == Alignment.CENTER:
                    formatted_cell: str = PrettyStrings.center(cell, widths[i])
                else:
                    left = self.cell_alignment < 0
                    formatted_cell: str = PrettyStrings.column(cell, widths[i], left)

                row_str_builder.append(formatted_cell)

                if self.show_vlines:
                    row_str_builder.append(self._VERTICAL_SEPARATOR)

            to_join: str = "" if self.show_vlines else " "
            table_str_builder.append(to_join.join(row_str_builder))

        table_str_builder.append(horizontal_frame)

        return "\n".join(table_str_builder)

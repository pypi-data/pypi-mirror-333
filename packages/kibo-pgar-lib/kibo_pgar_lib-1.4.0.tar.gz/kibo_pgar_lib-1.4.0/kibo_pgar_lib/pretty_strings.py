"""Module for the PrettyStrings class"""

from kibo_pgar_lib.ansi_colors import (
    AnsiFontColors,
    AnsiFontWeights,
    AnsiFontDecorations,
    RESET,
)


class PrettyStrings:
    """This class contains various methods to prettify print strings to the terminal."""

    _ERRORS: dict[str, str] = {
        "constructor": "This class is not instantiable!",
        "empty_char": "Character mustn't be an empty string.\n",
    }

    _SPACE = " "
    _HORIZONTAL_FRAME = "-"
    _VERTICAL_FRAME = "|"
    _NEW_LINE = "\n"

    def __init__(self) -> None:
        """Prevents the instantiation of this class.

        Raises
        ------
        - `NotImplementedError`
        """
        raise NotImplementedError(PrettyStrings._ERRORS["constructor"])

    @staticmethod
    def frame(
        to_frame: str, frame_length: int, centered: bool, vertical_frame: bool
    ) -> str:
        """Puts the given string in the center or in the beginning of the line surrounded by the
        horizontal frame above and below and, if needed, also the vertical frame before and after.
        It's required to specify a frame length for the horizontal frame.

        Params
        ------
        - `to_frame` -> The string to put in the frame
        - `frame_length` -> The length of the horizontal frame.
        - `centered` -> If the string needs to be centered or not.
        - `vertical_frame` -> If the vertical frame is needed or not.

        Returns
        -------
        A string containing the framed original string.
        """
        framed: list[str] = []
        horizontal_frame: list[str] = [
            PrettyStrings.repeat_char(PrettyStrings._HORIZONTAL_FRAME, frame_length),
            PrettyStrings._NEW_LINE,
        ]

        framed.extend(horizontal_frame)

        to_append: list[str] = [PrettyStrings._NEW_LINE]
        if vertical_frame:
            frame_length -= 2

            to_append.extend(
                [PrettyStrings._VERTICAL_FRAME, PrettyStrings._VERTICAL_FRAME]
            )
            to_append.reverse()

            insert_pos_framed_str = 1
        else:
            insert_pos_framed_str = 0

        framed_str: str = (
            PrettyStrings.center(to_frame, frame_length)
            if centered
            else PrettyStrings.column(to_frame, frame_length)
        )
        to_append.insert(insert_pos_framed_str, framed_str)

        framed.append("".join(to_append))

        framed.extend(horizontal_frame)

        return "".join(framed)

    @staticmethod
    def column(to_columnize: str, width: int, left: bool = True) -> str:
        """Puts teh given string at the beginning of the line and adds spaces until the end of it.
        If the string is too long for the width of the line, it will be cut off.

        Params
        ------
        - `to_columnize` -> The string to put in column.
        - `width` -> The length of the line.
        - `left` -> If the alignment should be on the left or right, defaulted to True.

        Returns
        -------
        A string containing the columned string.
        """
        to_columnize_length = len(to_columnize)
        chars_to_print: int = min(width, to_columnize_length)

        columned: str = (
            to_columnize[:chars_to_print]
            if to_columnize_length > chars_to_print
            else to_columnize
        )
        spaces: str = PrettyStrings.repeat_char(
            PrettyStrings._SPACE, width - to_columnize_length
        )

        if left:
            return "".join([columned, spaces])

        return "".join([spaces, columned])

    @staticmethod
    def center(to_center: str, width: int) -> str:
        """Puts the given string in the center of the line of the given width. If the string is too
        long it will be cut off.

        Params
        ------
        - `to_center` -> The string to center.
        - `width` -> The length of the line where to center the string.

        Returns
        -------
        A string containing the centered string.
        """
        to_center_length = len(to_center)

        if to_center_length > width:
            return to_center[:width]

        if to_center_length == width:
            return to_center

        whitespaces_num = width - to_center_length
        whitespaces_before = whitespaces_num // 2
        whitespaces_after = whitespaces_num - whitespaces_before

        centered: list[str] = [
            PrettyStrings.repeat_char(PrettyStrings._SPACE, whitespaces_before),
            to_center,
            PrettyStrings.repeat_char(PrettyStrings._SPACE, whitespaces_after),
        ]

        return "".join(centered)

    @staticmethod
    def repeat_char(char: str, times: int) -> str:
        """Repeats a given character a given number of times.

        Params
        ------
        - `char` -> The character to repeat.
        - `times` -> The number of times to repeat the character.

        Returns
        -------
        A string containing the character repeated. If times is less than or equal to 0 an empty
        string will be returned.

        Raises
        ------
        - `ValueError` -> If `char` is an empty string.
        """
        if not char:
            raise ValueError(PrettyStrings._ERRORS["empty_char"])

        return char[0] * max(0, times)

    @staticmethod
    def isolated_line(to_isolate: str) -> str:
        """Isolates a given string by adding an empty line before and after it.

        Params
        ------
        - `to_isolate` -> The string to isolate.

        Returns
        -------
        A string containing the isolated string.
        """
        isolated = [
            PrettyStrings._NEW_LINE,
            to_isolate,
            PrettyStrings._NEW_LINE,
        ]

        return "".join(isolated)

    @staticmethod
    def prettify(
        to_prettify: str,
        color: AnsiFontColors = None,
        weight: AnsiFontWeights = None,
        decoration: AnsiFontDecorations = None,
    ) -> str:
        """Prettifies the given string by adding a color, weight and decoration if given.

        Params
        ------
        - `to_prettify` -> The string to be prettified.
        - `color` -> The color given to the string, `none` for default color.
        - `weight` -> The weight given to the string, `none` for default weight.
        - `decoration` -> The decoration given to the string, `none` for default decoration.

        Returns
        -------
        A string representing the given one prettified.
        """
        prettified: list[str] = []
        reset = False

        if color:
            reset = True
            prettified.append(color)

        if weight:
            reset = True
            prettified.append(weight)

        if decoration:
            reset = True
            prettified.append(decoration)

        prettified.append(to_prettify)

        if reset:
            prettified.append(RESET)

        return "".join(prettified)

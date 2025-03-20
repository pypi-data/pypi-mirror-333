"""Module representing the FileService class"""

# Standard Modules
import pickle

# Internal Modules
from kibo_pgar_lib.pretty_strings import PrettyStrings
from kibo_pgar_lib.ansi_colors import AnsiFontColors, AnsiFontWeights


class FileService:
    """
    This class has useful methods to serialize/deserialize objects and save/load them to/from a
    file.
    """

    _ERRORS: dict[str, str] = {
        "red": PrettyStrings.prettify(
            "Error!", AnsiFontColors.RED, AnsiFontWeights.BOLD
        ),
        "constructor": "This class is not instantiable!",
        "file_not_found": "Can't find the file %s\n",
        "reading": "Problem reading the file %s\n",
        "writing": "Problem writing the file %s\n",
    }

    def __init__(self) -> None:
        """Prevents instantiation of this class

        Raises
        ------
        - `NotImplementedError`
        """

        raise NotImplementedError(FileService._ERRORS["constructor"])

    @staticmethod
    def serialize_object(file_path: str, to_save: object) -> None:
        """Serialize to file whatever object is given.

        Params
        ------
        - `file_path` -> The file path where to save the serialized object.
        - `to_save` -> The object to serialize and save.
        """

        try:
            with open(file_path, "wb") as f:
                pickle.dump(to_save, f)
        except IOError:
            print(FileService._ERRORS["red"])
            print(FileService._ERRORS["writing"] % file_path)

    @staticmethod
    def deserialize_object(file_path: str) -> object:
        """Deserialize whatever object is saved in the given file.

        Params
        ------
        - `file_path` -> The file path where to find the serialized object.

        Returns
        -------
        An instance of the deserialized object.
        """

        try:
            with open(file_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print(FileService._ERRORS["red"])
            print(FileService._ERRORS["file_not_found"] % file_path)
        except (IOError, pickle.UnpicklingError):
            print(FileService._ERRORS["red"])
            print(FileService._ERRORS["reading"] % file_path)

        return None

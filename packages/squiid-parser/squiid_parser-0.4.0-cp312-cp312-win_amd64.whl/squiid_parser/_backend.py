from __future__ import annotations

import ctypes
import pathlib
import platform
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from os import PathLike

from squiid_parser._data_structs import ParserError, ParseResult_FFI

COMPATIBLE_PARSER_VERSION: Final[bytes] = b">=1.4.0,<2.0"


class SquiidParser:
    """Class used to access the Squiid parsing engine."""

    def __init__(self, library_path: str | PathLike[str] | None = None) -> None:
        """Construct a new Squiid parser class.

        Args:
            library_path (str | PathLike[str] | None): path to `libsquiid_parser.so`
        """
        if library_path is None:
            file_directory = pathlib.Path(__file__).parent.resolve()

            prefix = "lib"
            extension = ".so"
            if platform.system() == "Windows":  # pragma: no cover
                prefix = ""
                extension = ".dll"
            elif platform.system() == "Darwin":  # pragma: no cover
                extension = ".dylib"

            resolved_library_path = (
                file_directory / f"{prefix}squiid_parser{extension}"
            ).resolve()
        else:
            resolved_library_path = pathlib.Path(library_path).resolve()

        # check if library exists before loading
        if not resolved_library_path.is_file():
            exception_message = f"Shared library not found at {resolved_library_path}"
            raise FileNotFoundError(exception_message)

        self._lib: ctypes.CDLL = ctypes.CDLL(str(resolved_library_path))

        # define arg types for functions
        self._lib.parse_exposed.argtypes = [
            ctypes.c_char_p,  # input string
        ]
        self._lib.parse_exposed.restype = ParseResult_FFI

        # Version check function
        self._lib.check_compatible.argtypes = [
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.POINTER(ctypes.c_char)),
        ]
        self._lib.check_compatible.restype = ctypes.c_bool

        # Cleanup functions
        self._lib.free_parse_result.argtypes = [ParseResult_FFI]
        self._lib.free_parse_result.restype = None

        self._lib.free_string.argtypes = [ctypes.c_char_p]
        self._lib.free_string.restype = None

        # check version compatibility with loaded library
        self._check_compatible()

    def parse(self, input_string: str) -> list[str]:
        """Parse an algebraic notation string into an RPN notation list of strings.

        Args:
            input_string (str): The algebraic string to parse.

        Returns:
            list[str]: The list of operation strings in RPN notation.

        Raises:
            ParserError: if an error is encountered during parsing.
        """
        # encode the input as bytes
        input_bytes = input_string.encode("utf-8")

        # try to parse the current string
        result_ffi: ParseResult_FFI = self._lib.parse_exposed(
            ctypes.c_char_p(input_bytes),
        )

        try:
            if result_ffi.error:
                raise ParserError(result_ffi.error)

            parsed_results: list[str] = []
            # iterate over the array of results
            for i in range(result_ffi.result_len):
                # get the current result value
                curr_value = ctypes.c_char_p(result_ffi.result[i]).value

                if curr_value is not None:  # pragma: no branch
                    # append it to the result list if not None
                    parsed_results.append(curr_value.decode("utf-8"))

            return parsed_results
        finally:
            # free the unneeded bytes once finished
            self._lib.free_parse_result(result_ffi)

    def _check_compatible(self) -> None:
        """Check version compatibility with the library.

        Raises:
            RuntimeError: If the versions are incompatible
        """
        error = ctypes.POINTER(ctypes.c_char)()
        if not self._lib.check_compatible(
            ctypes.c_char_p(COMPATIBLE_PARSER_VERSION),
            ctypes.byref(error),
        ):
            # copy the error and free the original
            error_copy = b""
            if error:  # pragma: no branch
                error_copy = ctypes.cast(error, ctypes.c_char_p).value or b""
                self._lib.free_string(error)

            raise RuntimeError(error_copy.decode())

        if error:
            self._lib.free_string(error)  # pragma: no cover

from ctypes import POINTER, Structure, c_char_p, c_int
from dataclasses import dataclass
from typing import final


@final
@dataclass
class ParseResult_FFI(Structure):
    """Structure containing the result of a parse operation done over FFI.

    Will contain either a result array or an error message, but not both.
    """

    _fields_ = [
        ("result", POINTER(c_char_p)),
        ("result_len", c_int),
        ("error", c_char_p),
    ]

    result: list[bytes]
    result_len: int
    error: bytes


class ParserError(Exception):
    """Generic error that can be encountered while parsing."""

"""Squiid parser bindings.

This module includes basic bindings to the Squiid parser that allow you to
parse a string into a list of tokens with the `parse` function
"""

from squiid_parser._backend import SquiidParser
from squiid_parser._data_structs import ParserError

__all__ = ["ParserError", "SquiidParser"]

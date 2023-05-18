"""Contains a check for proper capitalization of the summary line."""

import string
from typing import Optional

from lintel import CHECKED_NODE_TYPES, Configuration, Docstring, DocstringError


class D403(DocstringError):
    description = "First word of the first line should be properly capitalized ({!r}, not {!r})."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D403"]:
        first_word: str = docstring.content.split()[0]

        if first_word in (first_word.upper(), first_word.capitalize()):
            return None

        if first_word.startswith("'"):
            return None

        for char in first_word:
            if char not in string.ascii_letters and char != "'":
                return None

        error = cls(node)
        error.parameters = [first_word.capitalize(), first_word]

        return error

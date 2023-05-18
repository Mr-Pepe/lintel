"""Contains a check whether a docstring starts with `This`."""

from typing import Optional

from lintel import (
    CHECKED_NODE_TYPES,
    Configuration,
    Docstring,
    DocstringError,
    strip_non_alphanumeric,
)


class D404(DocstringError):
    description = "First word of the docstring should not be `This`."
    explanation = """Docstrings should use short, simple language. They should not begin
                     with "This class is [..]" or "This module contains [..]".
                     """

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D404"]:
        stripped = docstring.content.strip()

        if not stripped:
            return None

        first_word = strip_non_alphanumeric(stripped.split()[0])

        if first_word.lower() == 'this':
            return cls(node)

        return None

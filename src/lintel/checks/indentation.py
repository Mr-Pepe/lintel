"""Contains a check for proper docstring indentation."""


from typing import Optional

from lintel import CHECKED_NODE_TYPES, Configuration, Docstring, DocstringError


class D206(DocstringError):
    description = "Docstring should be indented with spaces, not tabs."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D206"]:
        if len(docstring.line_indents) == 0:
            return None

        if "\t" in docstring.indent or any(
            "\t" in line_indent for line_indent in docstring.line_indents
        ):
            return cls(node)

        return None


class D207(DocstringError):
    description = "Docstring is under-indented."
    explanation = (
        "The entire docstring should be indented the same as the quotes at its first line."
    )

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D207"]:
        if len(docstring.line_indents) == 0:
            return None

        if min(docstring.line_indents) < docstring.indent:
            return cls(node)

        return None


class D208(DocstringError):
    description = "Docstring is over-indented."
    explanation = (
        "The entire docstring should be indented the same as the quotes at its first line."
    )

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D208"]:
        if len(docstring.line_indents) == 0:
            return None

        if (
            len(docstring.line_indents) > 1 and min(docstring.line_indents[:-1]) > docstring.indent
        ) or docstring.line_indents[-1] > docstring.indent:
            return cls(node)

        return None

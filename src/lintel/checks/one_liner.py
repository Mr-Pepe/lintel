"""Contains a check for one-liner docstrings."""


from typing import Optional

from astroid import NodeNG

from lintel import CHECKED_NODE_TYPES, Configuration, Docstring, DocstringError, has_content


class D200(DocstringError):
    description = "One-line docstring should fit on one line with quotes (found {} lines)."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D200"]:
        non_empty_lines = sum(1 for l in docstring.lines if has_content(l))

        # If docstring should be a one-liner but has multiple lines
        if non_empty_lines == 1 and len(docstring.lines) > 1:
            error = cls(node)
            error.parameters = [len(docstring.lines)]

            return error

        return None

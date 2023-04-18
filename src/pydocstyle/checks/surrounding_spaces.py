"""Contains checks for whitespaces surrounding a docstring."""


from typing import List, Optional

from pydocstyle import CHECKED_NODE_TYPES, Configuration, Docstring, DocstringError


class D210(DocstringError):
    description = "No whitespaces surrounding the docstring text are allowed."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Optional[Docstring], config: Configuration
    ) -> None:
        if (
            docstring.lines[0].startswith(' ')
            or len(docstring.lines) == 1
            and docstring.lines[0].endswith(' ')
        ):
            raise cls(node)

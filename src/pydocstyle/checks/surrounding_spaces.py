"""Contains checks for whitespaces surrounding a docstring."""


from typing import List, Optional

from pydocstyle import CHECKED_NODE_TYPES, Configuration, Docstring, DocstringError


class D210(DocstringError):
    description = "No whitespaces surrounding the docstring text are allowed."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Optional[Docstring], config: Configuration
    ) -> None:
        lines = docstring.content.split('\n')

        if lines[0].startswith(' ') or len(lines) == 1 and lines[0].endswith(' '):
            raise cls(node)

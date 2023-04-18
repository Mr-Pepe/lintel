"""Contains a docstring class."""

import linecache
import re
from typing import List, Optional

from pydocstyle import CHECKED_NODE_TYPES, has_content, leading_space, pairwise


class Docstring:
    """A docstring representation."""

    def __init__(self, parent_node: CHECKED_NODE_TYPES):
        """Initialize the docstring.

        Args:
            parent_node: The node that the docstring is attached to.

        Raises:
            ValueError: If the parent node does not have a doc node.
        """
        if parent_node.doc_node is None:
            raise ValueError(f"Node '{parent_node.name}' does not have a doc node.")

        self.parent_node = parent_node
        self.node = parent_node.doc_node

    @property
    def content(self) -> str:
        """The docstring content."""
        return str(self.node.value).expandtabs()

    @property
    def raw(self) -> str:
        """The raw docstring lines."""
        return "\n".join(
            l.rstrip()
            for l in linecache.getlines(self.parent_node.root().file)[
                self.node.fromlineno - 1 : self.node.end_lineno
            ]
        )

    @property
    def lines(self) -> List[str]:
        return self.content.strip().split('\n')

    @property
    def indent(self) -> str:
        """The indentation used for the first line of the docstring."""
        # Get the text before the quotation marks on the first line of the docstring
        pre_text = re.findall("(.*?)[uU]?[rR]?(\"\"\"|\'\'\')", self.raw.splitlines()[0])[0][0]

        return "".join(' ' for _ in pre_text)

    @property
    def line_indents(self) -> List[str]:
        """The indentation of non-empty lines in the docstring."""
        lines = [
            next_line
            for first_line, next_line in pairwise(self.raw.split("\n"), "")
            if has_content(next_line) and not first_line.endswith("\\")
        ]

        line_indents = [leading_space(l) for l in lines]

        return line_indents

    def __repr__(self) -> str:
        return f'"""{self.content}"""'


def get_docstring_from_doc_node(
    node: CHECKED_NODE_TYPES,
) -> Optional[Docstring]:
    """Retrieve the docstring of an astroid node."""
    if node.doc_node is None:
        return None

    return Docstring(node)

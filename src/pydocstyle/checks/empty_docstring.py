"""Contains a check for empty docstrings."""


from typing import Optional

from astroid import NodeNG

from pydocstyle import (
    CHECKED_NODE_TYPES,
    NODES_TO_CHECK,
    Configuration,
    Docstring,
    DocstringError,
    has_content,
)


class D419(DocstringError):
    description = "Docstring is empty."
    applicable_nodes = NODES_TO_CHECK
    applicable_if_doc_string_is_empty = True
    terminal = True

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Optional[Docstring], config: Configuration
    ) -> None:
        if not has_content(docstring.content):
            return cls(node)

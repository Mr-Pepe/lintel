"""Docstring violation definition."""

from __future__ import annotations

import os
from typing import List, Optional

from astroid import ClassDef, FunctionDef, Module

from pydocstyle import (
    CHECKED_NODE_TYPES,
    NODES_TO_CHECK,
    Configuration,
    Docstring,
    get_docstring_from_doc_node,
)


class DocstringError(Exception):
    """Linting error in docstring."""

    description: str
    explanation: str
    applicable_nodes: List[CHECKED_NODE_TYPES] = NODES_TO_CHECK
    applicable_if_doc_string_is_missing = False
    applicable_if_doc_string_is_empty = False
    terminal = False

    def __init__(
        self,
        node: CHECKED_NODE_TYPES,
    ) -> None:
        """Initialize the error."""
        self.node = node

    @classmethod
    def error_code(cls) -> str:
        return cls.__name__

    @property
    def file_name(self):
        """Return the file this error originates from."""
        return os.path.normcase(self.node.root().file)

    @property
    def line(self):
        """Return the line this error originates from."""
        return self.node.lineno

    @property
    def node_name(self):
        """Return the node this error originates from."""
        return self.node.name

    @property
    def node_type(self):
        """Return the node type this error belongs to."""
        return {Module: "module", FunctionDef: "function", ClassDef: "class"}[type(self.node)]

    def __str__(self) -> str:
        """Return the string output for this error."""
        return f"{self.file_name}:{self.line} in {self.node_type} '{self.node_name}': {self.error_code()} - {self.description}"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def check(cls, node: CHECKED_NODE_TYPES, config: Configuration) -> None:
        """Implement the actual check logic in the :py:meth:`.check_implementation` method."""

        if not isinstance(node, cls.applicable_nodes):
            return None

        if node.doc_node is None and not cls.applicable_if_doc_string_is_missing:
            return None

        docstring = get_docstring_from_doc_node(node)

        if (
            docstring is not None
            and docstring.content == ""
            and not cls.applicable_if_doc_string_is_empty
        ):
            return None

        cls.check_implementation(node, docstring, config)

    @classmethod
    def check_implementation(
        cls,
        node: CHECKED_NODE_TYPES,
        docstring: Optional[Docstring],
        config: Configuration,
    ) -> None:
        """Check a docstring."""
        raise NotImplementedError()

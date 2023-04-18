"""Docstring violation definition."""

from __future__ import annotations

import os
from typing import Any, List, Optional, Union

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
    """Gets printed to the console when an error is encountered.
    The description is formatted using the provided `parameters`."""
    explanation: str = ""
    """A more detailed explanation of the error."""
    applicable_nodes: Union[CHECKED_NODE_TYPES, List[CHECKED_NODE_TYPES]] = NODES_TO_CHECK
    """The node classes this error is applicable for."""
    applicable_if_doc_string_is_missing = False
    """Whether this error should be checked for if the node does not have a docstring."""
    applicable_if_doc_string_is_empty = False
    """Whether this error should be checked for if the node's docstring is empty."""
    terminal = False
    """Whether this error should skip subsequent error checks for a node."""
    parameters: Optional[list[Any]] = None
    """Parameters used for formatting the description."""

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
    def node_type(self) -> CHECKED_NODE_TYPES:
        """Return the node type this error belongs to."""
        return {Module: "module", FunctionDef: "function", ClassDef: "class"}[type(self.node)]

    @property
    def message(self) -> str:
        """Returns the error message without context about the file."""
        if self.parameters is None:
            self.parameters = []

        return f"{self.error_code()}: {self.description.format(*self.parameters)}"

    def __str__(self) -> str:
        """Return the string output for this error."""

        return (
            f"{self.file_name}:{self.line} in {self.node_type} '{self.node_name}' -> "
            + self.message
        )

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def check(cls, node: CHECKED_NODE_TYPES, config: Configuration) -> None:
        """Implement the actual check logic in the :py:meth:`.check_implementation` method."""

        if not isinstance(node, cls.applicable_nodes):
            return None

        docstring = get_docstring_from_doc_node(node)

        if docstring is None and not cls.applicable_if_doc_string_is_missing:
            return None

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

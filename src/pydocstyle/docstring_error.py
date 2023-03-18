"""Docstring violation definition."""

from __future__ import annotations

import linecache
import os
from itertools import dropwhile

from astroid import ClassDef, FunctionDef, Module

from pydocstyle.utils import CHECKED_NODE_TYPE

from .utils import is_blank

__all__ = ('Error', 'ErrorRegistry')


class DocstringError(Exception):
    """Linting error in docstring."""

    error_code: str
    description: str
    explanation: str

    def __init__(
        self,
        node: CHECKED_NODE_TYPE,
    ) -> None:
        """Initialize the error."""
        self.node = node

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
        return {Module: "module", FunctionDef: "function", ClassDef: "class"}[
            type(self.node)
        ]

    def __str__(self) -> str:
        """Return the string output for this error."""
        return f"{self.file_name}:{self.line} in {self.node_type} '{self.node_name}': {self.error_code} - {self.description}"

    def __repr__(self) -> str:
        return str(self)

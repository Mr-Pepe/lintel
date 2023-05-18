"""Contains a blank line checks."""

import linecache
from itertools import takewhile
from typing import List, Optional, Tuple, Union

import astroid

from lintel import (
    CHECKED_NODE_TYPES,
    Configuration,
    Docstring,
    DocstringError,
    has_content,
    is_blank,
)


class D201(DocstringError):
    description = "No blank lines allowed before function/method docstring (found {})."
    applicable_nodes = astroid.FunctionDef

    @classmethod
    def check_implementation(
        cls, function_: astroid.FunctionDef, docstring: Docstring, config: Configuration
    ) -> Optional["D201"]:
        n_blanks_before = _get_n_blanks_before_docstring(function_)

        if n_blanks_before != 0:
            error = cls(function_)
            error.parameters = [n_blanks_before]

            return error

        return None


class D202(DocstringError):
    description = "No blank lines allowed after function/method docstring (found {})."
    applicable_nodes = astroid.FunctionDef

    @classmethod
    def check_implementation(
        cls, function_: astroid.FunctionDef, docstring: Docstring, config: Configuration
    ) -> Optional["D202"]:
        lines_after, _, n_blanks_after = _get_stuff_after_docstring(function_)

        if (
            n_blanks_after != 0
            and not _is_empty_definition(lines_after, n_blanks_after)
            and not _blank_line_followed_by_inner_function_or_class(lines_after, n_blanks_after)
        ):
            error = cls(function_)
            error.parameters = [n_blanks_after]

            return error

        return None


class D203(DocstringError):
    description = "Class docstrings should have 1 blank line before them (found {})."
    applicable_nodes = astroid.ClassDef

    @classmethod
    def check_implementation(
        cls, class_: astroid.ClassDef, docstring: Docstring, config: Configuration
    ) -> Optional["D203"]:
        n_blanks_before = _get_n_blanks_before_docstring(class_)

        if n_blanks_before != 1:
            error = cls(class_)
            error.parameters = [n_blanks_before]

            return error

        return None


class D204(DocstringError):
    description = "1 blank line required after class docstring (found {})."
    applicable_nodes = astroid.ClassDef

    @classmethod
    def check_implementation(
        cls, class_: astroid.ClassDef, docstring: Docstring, config: Configuration
    ) -> Optional["D204"]:
        lines_after, _, n_blanks_after = _get_stuff_after_docstring(class_)

        if n_blanks_after != 1 and not _is_empty_definition(lines_after, n_blanks_after):
            error = cls(class_)
            error.parameters = [n_blanks_after]

            return error

        return None


class D205(DocstringError):
    description = "1 blank line required between summary line and description (found {})."
    explanation = """Multi-line docstrings consist of a summary line just like a one-line
                     docstring, followed by a blank line, followed by a more elaborate
                     description."""

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D205"]:
        lines = docstring.content.strip().split('\n')

        if len(lines) <= 1:
            return None

        blanks = list(takewhile(is_blank, lines[1:]))
        n_blanks = len(blanks)

        if n_blanks != 1:
            error = cls(node)
            error.parameters = [n_blanks]

            return error

        return None


class D211(DocstringError):
    description = "No blank lines allowed before class docstring (found {})."
    applicable_nodes = astroid.ClassDef

    @classmethod
    def check_implementation(
        cls, class_: astroid.ClassDef, docstring: Docstring, config: Configuration
    ) -> Optional["D211"]:
        n_blanks_before = _get_n_blanks_before_docstring(class_)

        if n_blanks_before != 0:
            error = cls(class_)
            error.parameters = [n_blanks_before]

            return error

        return None


def _get_n_blanks_before_docstring(node: Union[astroid.FunctionDef, astroid.ClassDef]) -> int:
    n_blanks = 0
    line = node.doc_node.fromlineno - 1

    while line > 0:
        if has_content(linecache.getline(node.root().file, line)):
            break

        n_blanks += 1
        line -= 1

    return n_blanks


def _get_stuff_after_docstring(
    node: Union[astroid.ClassDef, astroid.FunctionDef]
) -> Tuple[List[str], List[str], int]:
    lines_after = [
        linecache.getline(node.root().file, l)
        for l in range(node.doc_node.end_lineno + 1, node.end_lineno + 2)
    ]
    blanks_after = list(takewhile(is_blank, lines_after))
    n_blanks_after = len(blanks_after)

    return lines_after, blanks_after, n_blanks_after


def _is_empty_definition(lines_after: List[str], n_blanks_after: int) -> bool:
    return n_blanks_after == 1 and len(lines_after) == 1


def _blank_line_followed_by_inner_function_or_class(
    lines_after: List[str], n_blanks_after: int
) -> bool:
    return (
        n_blanks_after == 1
        and len(lines_after) > 1
        and lines_after[1].lstrip().startswith(("class", "def", "async def", "@"))
    )

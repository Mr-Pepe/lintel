"""Contains checks for the correct amount of blank lines after a docstring."""

import linecache
from itertools import takewhile
from typing import List, Optional, Tuple, Union

from astroid import ClassDef, FunctionDef

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import is_blank
from pydocstyle.violations import D202, D204


@check(FunctionDef)
def check_no_blank_lines_after_function_docstring(
    function_: FunctionDef, __: Docstring, _: Configuration
) -> Optional[D202]:
    """D202: No blank lines allowed after function/method docstring.

    There should be no blank line after the docstring unless directly
    followed by an inner function or class.
    """
    lines_after, _, n_blanks_after = _get_stuff_after_docstring(function_)

    if n_blanks_after == 0:
        return None

    if _is_empty_definition(lines_after, n_blanks_after):
        return None

    if _blank_line_followed_by_inner_function_or_class(
        lines_after, n_blanks_after
    ):
        return None

    return D202(n_blanks_after)


@check(ClassDef)
def check_single_blank_line_after_class_docstring(
    class_: ClassDef, _: Docstring, __: Configuration
) -> Optional[D204]:
    """D204: 1 blank line required after class docstring."""
    lines_after, _, n_blanks_after = _get_stuff_after_docstring(class_)

    if _is_empty_definition(lines_after, n_blanks_after):
        return None

    if n_blanks_after != 1:
        return D204(n_blanks_after)

    return None


def _get_stuff_after_docstring(
    node: Union[ClassDef, FunctionDef]
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
        and lines_after[1]
        .lstrip()
        .startswith(("class", "def", "async def", "@"))
    )

"""Contains checks for the correct amount of blank lines before a docstring."""


import linecache
from typing import List, Optional, Tuple, Union

from astroid import ClassDef, FunctionDef

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import has_content
from pydocstyle.violations import D201, D203, D211


@check(FunctionDef)
def check_no_blank_lines_before_function_docstring(
    function_: FunctionDef, docstring: Docstring, config: Configuration
) -> Optional[D201]:
    """D201 No blank lines allowed before function/method docstring."""
    n_blanks_before = _get_n_blanks_before_docstring(function_, docstring)

    if n_blanks_before == 0:
        return None

    return D201(n_blanks_before)


@check(ClassDef)
def check_single_blank_line_before_class_docstring(
    class_: ClassDef, docstring: Docstring, config: Configuration
) -> Optional[D203]:
    """D203: Class docstrings should have 1 blank line before them."""
    n_blanks_before = _get_n_blanks_before_docstring(class_, docstring)

    if n_blanks_before == 1:
        return None

    return D203(n_blanks_before)


@check(ClassDef)
def check_no_blank_lines_before_class_docstring(
    class_: ClassDef, docstring: Docstring, config: Configuration
) -> Optional[D211]:
    """D211: No blank lines allowed before class docstring."""
    n_blanks_before = _get_n_blanks_before_docstring(class_, docstring)

    if n_blanks_before == 0:
        return None

    return D211(n_blanks_before)


def _get_n_blanks_before_docstring(
    node: Union[FunctionDef, ClassDef], docstring: Docstring
) -> int:
    n_blanks = 0
    line = node.doc_node.fromlineno - 1

    while line > 0:
        if has_content(linecache.getline(node.root().file, line)):
            break

        n_blanks += 1
        line -= 1

    return n_blanks

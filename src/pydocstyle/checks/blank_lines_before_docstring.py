from itertools import takewhile
from typing import List, Optional, Tuple

from pydocstyle.checks import check
from pydocstyle.parser import Class, Definition, Function
from pydocstyle.utils import is_blank
from pydocstyle.violations import D201, D203, D211


@check(Function)
def check_no_blank_lines_before_function_docstring(
    function: Function, docstring: str
) -> Optional[D201]:
    """D201 No blank lines allowed before function/method docstring."""
    if not docstring:
        return None

    _, _, n_blanks_before = _get_stuff_before_docstring(function, docstring)

    if n_blanks_before == 0:
        return None

    return D201(n_blanks_before)


@check(Class)
def check_single_blank_line_before_class_docstring(
    class_: Class, docstring: str
) -> Optional[D203]:
    """D203: Class docstrings should have 1 blank line before them."""
    if not docstring:
        return None

    _, _, n_blanks_before = _get_stuff_before_docstring(class_, docstring)

    if n_blanks_before == 1:
        return None

    return D203(n_blanks_before)


@check(Class)
def check_no_blank_lines_before_class_docstring(
    class_: Class, docstring: str
) -> Optional[D211]:
    """D211: No blank lines allowed before class docstring."""
    if not docstring:
        return None

    _, _, n_blanks_before = _get_stuff_before_docstring(class_, docstring)

    if n_blanks_before == 0:
        return None

    return D211(n_blanks_before)


def _get_stuff_before_docstring(
    definition: Definition, docstring: str
) -> Tuple[List[str], List[str], int]:
    lines_before = definition.source.partition(docstring)[0].split('\n')[:-1]
    blanks_before = list(takewhile(is_blank, reversed(lines_before)))
    n_blanks_before = len(blanks_before)

    return lines_before, blanks_before, n_blanks_before

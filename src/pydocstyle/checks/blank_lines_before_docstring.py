from itertools import takewhile
from typing import Optional

from pydocstyle.checks import check
from pydocstyle.parser import Function
from pydocstyle.utils import is_blank
from pydocstyle.violations import D201


@check(Function)
def check_blank_lines_before_docstring(
    function: Function, docstring: str
) -> Optional[D201]:
    """D201 No blank lines allowed before function/method docstring."""
    if not docstring:
        return None

    lines_before = function.source.partition(docstring)[0].split('\n')[:-1]
    blanks_before = list(takewhile(is_blank, reversed(lines_before)))
    n_blanks_before = len(blanks_before)

    if n_blanks_before == 0:
        return None

    return D201(n_blanks_before)

from itertools import takewhile
from typing import List, Optional

from pydocstyle.checks import check
from pydocstyle.parser import Function
from pydocstyle.utils import is_blank
from pydocstyle.violations import D202


@check(Function)
def check_blank_lines_after_docstring(
    function: Function, docstring: str
) -> Optional[D202]:
    """D202: No blank lines allowed after function/method docstring.

    There should be no blank line after the docstring unless directly
    followed by an inner function or class.
    """
    if not docstring:
        return None

    lines_after = function.source.partition(docstring)[-1].split('\n')[1:]
    blanks_after = list(takewhile(is_blank, lines_after))
    n_blanks_after = len(blanks_after)

    if n_blanks_after == 0:
        return None

    if _is_empty_function(lines_after, n_blanks_after):
        return None

    if _blank_line_followed_by_inner_function_or_class(
        lines_after, n_blanks_after
    ):
        return None

    return D202(n_blanks_after)


def _is_empty_function(lines_after: List[str], n_blanks_after: int) -> bool:
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

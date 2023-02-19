from itertools import takewhile
from typing import List, Optional, Tuple

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.parser import Class, Definition, Function
from pydocstyle.utils import is_blank
from pydocstyle.violations import D202, D204


@check(Function)
def check_no_blank_lines_after_function_docstring(
    function: Function, docstring: str, config: Configuration
) -> Optional[D202]:
    """D202: No blank lines allowed after function/method docstring.

    There should be no blank line after the docstring unless directly
    followed by an inner function or class.
    """
    if not docstring:
        return None

    lines_after, _, n_blanks_after = _get_stuff_after_docstring(
        function, docstring
    )

    if n_blanks_after == 0:
        return None

    if _is_empty_definition(lines_after, n_blanks_after):
        return None

    if _blank_line_followed_by_inner_function_or_class(
        lines_after, n_blanks_after
    ):
        return None

    return D202(n_blanks_after)


@check(Class)
def check_single_blank_line_after_class_docstring(
    class_: Class, docstring: str, config: Configuration
) -> Optional[D204]:
    """D204: 1 blank line required after class docstring."""
    if not docstring:
        return None

    lines_after, _, n_blanks_after = _get_stuff_after_docstring(
        class_, docstring
    )

    if _is_empty_definition(lines_after, n_blanks_after):
        return None

    if n_blanks_after != 1:
        return D204(n_blanks_after)

    return None


def _get_stuff_after_docstring(
    definition: Definition, docstring: str
) -> Tuple[List[str], List[str], int]:
    lines_after = definition.source.partition(docstring)[-1].split('\n')[1:]
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

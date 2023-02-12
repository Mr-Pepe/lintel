import ast
from itertools import takewhile
from typing import Optional

from pydocstyle.checks import check
from pydocstyle.parser import Definition
from pydocstyle.utils import is_blank
from pydocstyle.violations import D205


@check(Definition)
def check_single_blank_line_after_summary(
    _: Definition, docstring: str
) -> Optional[D205]:
    """D205: Put one blank line between summary line and description.

    Multi-line docstrings consist of a summary line just like a one-line
    docstring, followed by a blank line, followed by a more elaborate
    description.
    """
    if not docstring:
        return None

    lines = ast.literal_eval(docstring).strip().split('\n')

    if len(lines) <= 1:
        return None

    blanks = list(takewhile(is_blank, lines[1:]))
    n_blanks = len(blanks)

    if n_blanks == 1:
        return None

    return D205(n_blanks)

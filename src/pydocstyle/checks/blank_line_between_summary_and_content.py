"""Contains a check for whether a summary line is followed by a blank line."""

from itertools import takewhile
from typing import Optional

from astroid import NodeNG

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import is_blank
from pydocstyle.violations import D205


@check(NodeNG)
def check_single_blank_line_after_summary(
    _: NodeNG, docstring: Docstring, __: Configuration
) -> Optional[D205]:
    """D205: Put one blank line between summary line and description.

    Multi-line docstrings consist of a summary line just like a one-line
    docstring, followed by a blank line, followed by a more elaborate
    description.
    """
    lines = docstring.content.strip().split('\n')

    if len(lines) <= 1:
        return None

    blanks = list(takewhile(is_blank, lines[1:]))
    n_blanks = len(blanks)

    if n_blanks == 1:
        return None

    return D205(n_blanks)

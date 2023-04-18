"""Contains a check whether closing quotes are on their own line."""

from typing import Optional

from astroid import NodeNG

from pydocstyle._config import Configuration
from pydocstyle._docstring import Docstring
from pydocstyle._docstring_error import D209
from pydocstyle._utils import is_blank
from pydocstyle.checks import check


@check(NodeNG)
def check_newline_after_last_paragraph(
    _: NodeNG, docstring: Docstring, config: Configuration
) -> Optional[D209]:
    """D209: Put multi-line docstring closing quotes on separate line.

    Unless the entire docstring fits on a line, place the closing
    quotes on a line by themselves.
    """
    lines = [l for l in docstring.content.split('\n')]

    if len(lines) <= 1:
        return None

    if is_blank(lines[-1]):
        return None

    return D209()

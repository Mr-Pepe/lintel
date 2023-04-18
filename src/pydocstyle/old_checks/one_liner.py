"""Contains a check for one-liner docstrings."""


from typing import Optional

from astroid import NodeNG

from pydocstyle._config import Configuration
from pydocstyle._docstring import Docstring
from pydocstyle._docstring_error import D200
from pydocstyle._utils import has_content
from pydocstyle.checks import check


@check(NodeNG)
def check_one_liner(_: NodeNG, docstring: Docstring, config: Configuration) -> Optional[D200]:
    """D200: One-liner docstrings have to fit on one line with quotes."""
    lines = docstring.content.split('\n')

    non_empty_lines = sum(1 for l in lines if has_content(l))

    # If docstring should be a one-liner but has multiple lines
    if non_empty_lines == 1 and len(lines) > 1:
        return D200(len(lines))

    return None

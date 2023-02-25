import ast
from typing import Optional

from astroid import NodeNG

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import has_content
from pydocstyle.violations import D200


@check(NodeNG)
def check_one_liner(
    _: NodeNG, docstring: Docstring, config: Configuration
) -> Optional[D200]:
    """D200: One-liner docstrings have to fit on one line with quotes."""
    lines = docstring.doc.split('\n')

    non_empty_lines = sum(1 for l in lines if has_content(l))

    # If docstring should be a one-liner but has multiple lines
    if non_empty_lines == 1 and len(lines) > 1:
        return D200(len(lines))

    return None

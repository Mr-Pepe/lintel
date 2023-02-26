from typing import Optional

from astroid import NodeNG

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import has_content, is_blank
from pydocstyle.violations import D209


@check(NodeNG)
def check_newline_after_last_paragraph(
    _: NodeNG, docstring: Docstring, config: Configuration
) -> Optional[D209]:
    """D209: Put multi-line docstring closing quotes on separate line.

    Unless the entire docstring fits on a line, place the closing
    quotes on a line by themselves.
    """
    lines = [l for l in docstring.doc.split('\n')]

    if len(lines) <= 1:
        return None

    if is_blank(lines[-1]):
        return None

    return D209()

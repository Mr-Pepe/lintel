from typing import Optional, Union

from astroid import NodeNG

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import is_blank
from pydocstyle.violations import D212, D213


@check(NodeNG)
def check_multi_line_summary_start(
    _: NodeNG, docstring: Docstring, __: Configuration
) -> Optional[Union[D212, D213]]:
    """D212, D213: Multi-line docstring must start on specific line.

    D212: Multi-line docstring summary should start at the first line.
    D213: Multi-line docstring summary should start at the second line.
    """
    lines = docstring.doc.split('\n')

    if len(lines) <= 1:
        return None

    if is_blank(lines[0]):
        return D212()

    return D213()

import ast
from typing import Optional, Union

from astroid import NodeNG

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.violations import D212, D213

START_TRIPLE = (
    '"""',
    "'''",
    'u"""',
    "u'''",
    'r"""',
    "r'''",
    'ur"""',
    "ur'''",
)


@check(NodeNG)
def check_multi_line_summary_start(
    _: NodeNG, docstring: Docstring, config: Configuration
) -> Optional[Union[D212, D213]]:
    """D212, D213: Multi-line docstring must start on specific line.

    D212: Multi-line docstring summary should start at the first line.
    D213: Multi-line docstring summary should start at the second line.
    """
    lines = docstring.doc.split('\n')

    if len(lines) <= 1:
        return None

    first = lines[0].strip().lower()

    if first in START_TRIPLE:
        return D212()

    return D213()

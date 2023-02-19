import ast
from typing import Optional, Union

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.parser import Definition
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


@check(Definition)
def check_multi_line_summary_start(
    _: Definition, docstring: str, config: Configuration
) -> Optional[Union[D212, D213]]:
    """D212, D213: Multi-line docstring must start on specific line.

    D212: Multi-line docstring summary should start at the first line.
    D213: Multi-line docstring summary should start at the second line.
    """
    if not docstring:
        return None

    lines = ast.literal_eval(docstring).split('\n')

    if len(lines) <= 1:
        return None

    first = docstring.split("\n")[0].strip().lower()

    if first in START_TRIPLE:
        return D212()

    return D213()

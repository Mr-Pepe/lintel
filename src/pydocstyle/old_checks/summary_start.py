"""Contains checks regarding the summary line start of a docstring."""


from typing import Optional, Union

from astroid import NodeNG

from pydocstyle._config import Configuration
from pydocstyle._docstring import Docstring
from pydocstyle._docstring_error import D212, D213
from pydocstyle._utils import is_blank
from pydocstyle.checks import check


@check(NodeNG)
def check_multi_line_summary_start(
    _: NodeNG, docstring: Docstring, __: Configuration
) -> Optional[Union[D212, D213]]:
    """D212, D213: Multi-line docstring must start on specific line.

    D212: Multi-line docstring summary should start at the first line.
    D213: Multi-line docstring summary should start at the second line.
    """
    lines = docstring.content.split('\n')

    if len(lines) <= 1:
        return None

    if is_blank(lines[0]):
        return D212()

    return D213()

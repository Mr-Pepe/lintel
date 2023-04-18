"""Contains checks for whitespaces surrounding a docstring."""


from typing import List, Optional

from astroid import NodeNG

from pydocstyle._config import Configuration
from pydocstyle._docstring import Docstring
from pydocstyle._docstring_error import D210
from pydocstyle.checks import check


@check(NodeNG)
def check_surrounding_whitespaces(
    _: NodeNG, docstring: Docstring, config: Configuration
) -> Optional[D210]:
    """D210: No whitespaces allowed surrounding docstring text."""
    lines: List[str] = docstring.content.split('\n')

    if lines[0].startswith(' ') or len(lines) == 1 and lines[0].endswith(' '):
        return D210()

    return None

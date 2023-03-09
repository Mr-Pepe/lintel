import ast
from typing import List, Optional

from astroid import NodeNG

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.violations import D210


@check(NodeNG)
def check_surrounding_whitespaces(
    _: NodeNG, docstring: Docstring, config: Configuration
) -> Optional[D210]:
    """D210: No whitespaces allowed surrounding docstring text."""
    lines: List[str] = docstring.content.split('\n')

    if lines[0].startswith(' ') or len(lines) == 1 and lines[0].endswith(' '):
        return D210()

    return None

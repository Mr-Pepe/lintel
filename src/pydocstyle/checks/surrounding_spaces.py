import ast
from typing import List, Optional

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.parser import Definition
from pydocstyle.violations import D210


@check(Definition)
def check_surrounding_whitespaces(
    _: Definition, docstring: str, config: Configuration
) -> Optional[D210]:
    """D210: No whitespaces allowed surrounding docstring text."""
    if not docstring:
        return None

    lines: List[str] = ast.literal_eval(docstring).split('\n')

    if lines[0].startswith(' ') or len(lines) == 1 and lines[0].endswith(' '):
        return D210()

    return None

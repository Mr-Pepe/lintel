from typing import Optional

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.parser import Definition
from pydocstyle.utils import has_content
from pydocstyle.violations import D209


@check(Definition)
def check_newline_after_last_paragraph(
    _: Definition, docstring: str, config: Configuration
) -> Optional[D209]:
    """D209: Put multi-line docstring closing quotes on separate line.

    Unless the entire docstring fits on a line, place the closing
    quotes on a line by themselves.
    """
    if not docstring:
        return None

    lines = [l for l in docstring.split('\n') if has_content(l)]

    if len(lines) <= 1:
        return None

    if lines[-1].strip() in ('"""', "'''"):
        return None

    return D209()

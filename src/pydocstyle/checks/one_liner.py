import ast
from curses.ascii import isblank
from typing import Optional

from pydocstyle.checks import check
from pydocstyle.parser import Definition
from pydocstyle.utils import has_content
from pydocstyle.violations import D200


@check(Definition)
def check_one_liner(_: Definition, docstring: str) -> Optional[D200]:
    """D200: One-liner docstrings have to fit on one line with quotes."""
    if not docstring:
        return None

    lines = ast.literal_eval(docstring).split('\n')

    non_empty_lines = sum(1 for l in lines if has_content(l))

    # If docstring should be a one-liner but has multiple lines
    if non_empty_lines == 1 and len(lines) > 1:
        return D200(len(lines))

    return None

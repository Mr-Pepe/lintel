import ast
from typing import Optional

from pydocstyle.checks import check
from pydocstyle.parser import Definition
from pydocstyle.utils import has_content
from pydocstyle.violations import D419


@check(Definition, terminal=True)
def check_empty_docstring(_: Definition, docstring: str) -> Optional[D419]:
    """D419: Docstring is empty."""
    if not docstring:
        return None

    if has_content(ast.literal_eval(docstring)):
        return None

    return D419()

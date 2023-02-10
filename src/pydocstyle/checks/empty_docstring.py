import ast

from pydocstyle.checks import check
from pydocstyle.parser import Definition
from pydocstyle.utils import is_blank
from pydocstyle.violations import D419


@check(Definition, terminal=True)
def check_empty_docstring(_, docstring):
    """D419: Docstring is empty."""
    if docstring and is_blank(ast.literal_eval(docstring)):
        return D419()

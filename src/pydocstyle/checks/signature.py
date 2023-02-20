import ast
from typing import Optional

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.parser import Function
from pydocstyle.violations import D402


@check(Function)
def check_not_signature(
    function: Function, docstring: str, _: Configuration
) -> Optional[D402]:
    """D402: First line should not be function's or method's "signature".

    The one-line docstring should NOT be a "signature" reiterating the
    function/method parameters (which can be obtained by introspection).
    """
    if not docstring:
        return None

    first_line = ast.literal_eval(docstring).strip().split('\n')[0]

    if f"{function.name}(" not in first_line.replace(' ', ''):
        return None

    return D402()

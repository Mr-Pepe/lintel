import ast
from typing import Optional

from astroid import FunctionDef

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.violations import D402


@check(FunctionDef)
def check_not_signature(
    function: FunctionDef, docstring: Docstring, _: Configuration
) -> Optional[D402]:
    """D402: First line should not be function's or method's "signature".

    The one-line docstring should NOT be a "signature" reiterating the
    function/method parameters (which can be obtained by introspection).
    """
    if not docstring:
        return None

    first_line = docstring.doc.strip().split('\n')[0]

    if f"{function.name}(" not in first_line.replace(' ', ''):
        return None

    return D402()

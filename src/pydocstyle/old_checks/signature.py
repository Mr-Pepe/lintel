"""Make sure that a function signature is not repeated in the docstring."""

from typing import Optional

from astroid import FunctionDef

from pydocstyle._config import Configuration
from pydocstyle._docstring import Docstring
from pydocstyle._docstring_error import D402
from pydocstyle.checks import check


@check(FunctionDef)
def check_not_signature(
    function: FunctionDef, docstring: Docstring, _: Configuration
) -> Optional[D402]:
    """D402: First line should not be function's or method's "signature".

    The one-line docstring should NOT be a "signature" reiterating the
    function/method parameters (which can be obtained by introspection).
    """
    first_line = docstring.content.strip().split('\n')[0]

    if f"{function.name}(" not in first_line.replace(' ', ''):
        return None

    return D402()

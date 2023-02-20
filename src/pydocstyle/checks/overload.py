from typing import Optional

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.parser import Function
from pydocstyle.violations import D418


@check(Function)
def check_overload(
    function: Function, docstring: str, _: Configuration
) -> Optional[D418]:
    """D418: Function decorated with @overload shouldn't contain a docstring.

    Functions that are decorated with @overload are definitions,
    and are for the benefit of the type checker only.
    """
    if not docstring:
        return None

    if not function.is_overload:
        return None

    return D418()

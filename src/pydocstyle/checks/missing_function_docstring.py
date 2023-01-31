from typing import Optional, Union

from pydocstyle.checks import check
from pydocstyle.parser import Function, Method
from pydocstyle.violations import D103


@check(Function, terminal=True)
def check_missing_function_docstring(
    function_: Function, docstring: str
) -> Optional[D103]:
    """D103: Public functions should have docstrings."""

    if isinstance(function_, Method):
        return None

    if not function_.is_public:
        return None

    if docstring:
        return None

    if function_.is_overload:
        return None

    return D103()

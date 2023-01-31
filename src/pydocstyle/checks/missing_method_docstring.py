from typing import Optional, Union

from pydocstyle.checks import check
from pydocstyle.parser import Method
from pydocstyle.violations import D101, D102, D105, D106, D107


@check(Method, terminal=True)
def check_missing_method_docstring(
    method: Method, docstring: str
) -> Optional[Union[D102, D105, D107]]:
    """D102, D105, D107: Public, magic and __init__ methods should have docstrings."""
    if not method.is_public:
        return None

    if docstring:
        return None

    if method.is_magic:
        return D105()

    if method.is_init:
        return D107()

    if method.is_overload:
        return None

    return D102()

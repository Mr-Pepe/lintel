"""Make sure that `@overload` functions are not documented."""

from typing import Optional

from astroid import FunctionDef

from pydocstyle import _docstring
from pydocstyle._config import Configuration
from pydocstyle._docstring_error import D418
from pydocstyle._utils import get_decorator_names, is_overloaded
from pydocstyle.checks import check


@check(FunctionDef, only_if_docstring_not_empty=False)
def check_overload(
    function_: FunctionDef, docstring: _docstring, _: Configuration
) -> Optional[D418]:
    """D418: Function decorated with @overload shouldn't contain a docstring.

    Functions that are decorated with @overload are definitions,
    and are for the benefit of the type checker only.
    """
    if not is_overloaded(function_):
        return None

    return D418()

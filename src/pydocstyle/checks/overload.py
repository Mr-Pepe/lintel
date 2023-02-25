from typing import Optional

from astroid import FunctionDef

from pydocstyle import docstring
from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.utils import get_decorator_names
from pydocstyle.violations import D418


@check(FunctionDef, only_if_docstring_not_empty=False)
def check_overload(
    function_: FunctionDef, docstring: docstring, _: Configuration
) -> Optional[D418]:
    """D418: Function decorated with @overload shouldn't contain a docstring.

    Functions that are decorated with @overload are definitions,
    and are for the benefit of the type checker only.
    """
    if "overload" in get_decorator_names(function_):
        return D418()

    return None

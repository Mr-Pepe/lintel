from typing import Optional

from pydocstyle.checks import check
from pydocstyle.parser import Module, Package
from pydocstyle.violations import D100


@check(Module, terminal=True)
def check_missing_module_docstring(
    module: Module, docstring: str
) -> Optional[D100]:
    """D100: Public modules should have docstrings."""
    if type(module) == Package:
        return None

    if not module.is_public:
        return None

    if docstring:
        return None

    return D100()

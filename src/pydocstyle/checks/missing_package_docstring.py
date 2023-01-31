from typing import Optional

from pydocstyle.checks import check
from pydocstyle.parser import Module, Package
from pydocstyle.violations import D104


@check(Package, terminal=True)
def check_missing_package_docstring(
    module: Module, docstring: str
) -> Optional[D104]:
    """D100: Public packages should have docstrings."""
    if not module.is_public:
        return None

    if docstring:
        return None

    return D104()

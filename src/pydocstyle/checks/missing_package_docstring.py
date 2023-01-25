from pydocstyle.checks import check
from pydocstyle.parser import Package
from pydocstyle.violations import D104


@check(Package, terminal=True)
def check_missing_package_docstring(self, module, docstring):
    """D100: Public packages should have docstrings."""
    if not docstring and module.is_public:
        return D104()

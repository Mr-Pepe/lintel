from pydocstyle.checks import check
from pydocstyle.parser import Module, Package
from pydocstyle.violations import D100


@check(Module, terminal=True)
def check_missing_module_docstring(self, module: Module, docstring: str):
    """D100: Public modules should have docstrings."""
    if type(module) == Package:
        return

    if not module.is_public:
        return

    if not docstring:
        return D100()

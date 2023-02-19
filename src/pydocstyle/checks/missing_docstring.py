from typing import Optional, Union

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.parser import (
    Class,
    Function,
    Method,
    Module,
    NestedClass,
    Package,
)
from pydocstyle.violations import (
    D100,
    D101,
    D102,
    D103,
    D104,
    D105,
    D106,
    D107,
)


@check(Module, terminal=True)
def check_missing_module_docstring(
    module: Module, docstring: str, config: Configuration
) -> Optional[D100]:
    """D100: Public modules should have docstrings."""
    if type(module) == Package:
        return None

    if not module.is_public:
        return None

    if docstring:
        return None

    return D100()


@check(Package, terminal=True)
def check_missing_package_docstring(
    module: Module, docstring: str, config: Configuration
) -> Optional[D104]:
    """D100: Public packages should have docstrings."""
    if not module.is_public:
        return None

    if docstring:
        return None

    return D104()


@check(Method, terminal=True)
def check_missing_method_docstring(
    method: Method, docstring: str, config: Configuration
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


@check(Function, terminal=True)
def check_missing_function_docstring(
    function_: Function, docstring: str, config: Configuration
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


@check((Class, NestedClass), terminal=True)
def check_missing_class_docstring(
    class_: Class, docstring: str, config: Configuration
) -> Optional[Union[D101, D106]]:
    """D101, D106: Public (nested) classes should have docstrings."""
    if not class_.is_public:
        return None

    if docstring:
        return None

    return D106() if isinstance(class_, NestedClass) else D101()

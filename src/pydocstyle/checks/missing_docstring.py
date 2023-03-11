"""Contains for checks for missing docstrings."""

from typing import Optional, Union

from astroid import ClassDef, FunctionDef, Module

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import (
    VARIADIC_MAGIC_METHODS,
    is_dunder,
    is_overloaded,
    is_private,
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


@check(Module, terminal=True, only_if_docstring_exists=False)
def check_missing_module_docstring(
    module: Module, docstring: Optional[Docstring], _: Configuration
) -> Optional[Union[D100, D104]]:
    """D100, D104: Public modules and packages should have docstrings."""
    if docstring or is_private(module):
        return None

    return D104() if module.package else D100()


@check(FunctionDef, terminal=True, only_if_docstring_exists=False)
def check_missing_function_docstring(
    function_: FunctionDef,
    docstring: Optional[Docstring],
    _: Configuration,
) -> Optional[Union[D102, D105, D107]]:
    """D102, D103, D105, D107: Public, magic, and __init__ methods and functions should have docstrings."""
    if docstring or is_private(function_) or is_overloaded(function_):
        return None

    if isinstance(function_.parent, FunctionDef):
        # Function is nested
        return None

    if function_.is_bound():
        if (
            is_dunder(function_)
            and not function_.name in VARIADIC_MAGIC_METHODS
        ):
            return D105()

        if function_.name == "__init__":
            return D107()

        return D102()

    return D103()


@check(ClassDef, terminal=True, only_if_docstring_exists=False)
def check_missing_class_docstring(
    class_: ClassDef, docstring: Optional[Docstring], _: Configuration
) -> Optional[Union[D101, D106]]:
    """D101, D106: Public (nested) classes should have docstrings."""
    if docstring or is_private(class_):
        return None

    return (
        D106()
        if isinstance(
            class_.parent, (FunctionDef, ClassDef)
        )  # Class is nested
        else D101()
    )

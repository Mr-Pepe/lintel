import importlib
import inspect
import pkgutil
from collections import Counter
from types import ModuleType
from typing import Generator, Iterator, List, Optional, Type

import pydocstyle.checks
from pydocstyle import Convention, DocstringError

convention_ignores = {
    Convention.PEP257: {
        'D203',
        'D212',
        'D213',
        'D214',
        'D215',
        'D404',
        'D405',
        'D406',
        'D407',
        'D408',
        'D409',
        'D410',
        'D411',
        'D413',
        'D415',
        'D416',
        'D417',
        'D418',
    },
    Convention.NUMPY: {
        'D107',
        'D203',
        'D212',
        'D213',
        'D402',
        'D413',
        'D415',
        'D416',
        'D417',
    },
    Convention.GOOGLE: {
        'D203',
        'D204',
        'D213',
        'D215',
        'D400',
        'D401',
        'D404',
        'D406',
        'D407',
        'D408',
        'D409',
        'D413',
    },
}


def get_checks() -> List[Type[DocstringError]]:
    """Discovers docstring checks in the 'pydocstyle.checks' namespace."""
    errors: List[DocstringError] = []

    for _, module_name, _ in _iter_namespace(pydocstyle.checks):
        module = importlib.import_module(module_name)

        errors.extend(_get_checks_from_module(module))

    counts = dict(Counter(error.error_code() for error in errors))
    duplicates = {key: value for key, value in counts.items() if value > 1}

    if len(duplicates) > 0:
        raise RuntimeError(
            ("Found duplicate definitions for the following error codes: {}".format(*duplicates))
        )

    return sorted(errors, key=lambda x: (not x.terminal, x.error_code()))


def get_error_codes(convention: Optional[Convention] = None) -> List[str]:
    """Returns the error codes of available checks."""
    error_codes = {check.error_code() for check in get_checks()}

    if convention:
        error_codes -= convention_ignores[convention]

    return error_codes


def _iter_namespace(ns_pkg: ModuleType) -> Iterator[pkgutil.ModuleInfo]:
    """Iterates over the modules in a given package namespace."""
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def _get_checks_from_module(
    module: ModuleType,
) -> Generator[Type[DocstringError], None, None]:
    for member in dir(module):
        candidate = getattr(module, member)
        if (
            inspect.isclass(candidate)
            and issubclass(candidate, DocstringError)
            and not candidate == DocstringError
        ):
            yield candidate

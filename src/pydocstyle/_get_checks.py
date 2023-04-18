import importlib
import inspect
import pkgutil
from collections import Counter
from types import ModuleType
from typing import Generator, Iterator, List, Type

import pydocstyle.checks
from pydocstyle import DocstringError


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

    return sorted(errors, key=lambda x: x.error_code())


def get_error_codes() -> List[str]:
    """Returns the error codes of all available checks."""
    return [check.error_code() for check in get_checks()]


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

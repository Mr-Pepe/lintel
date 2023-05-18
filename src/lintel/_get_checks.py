import importlib
import inspect
import pkgutil
from collections import Counter
from functools import lru_cache
from types import ModuleType
from typing import Generator, Iterator, List, Set, Type

import lintel.checks
from lintel import DocstringError


@lru_cache
def get_checks() -> List[Type[DocstringError]]:
    """Discovers docstring checks in the 'lintel.checks' namespace."""
    errors: List[Type[DocstringError]] = []

    for _, module_name, _ in _iter_namespace(lintel.checks):
        module = importlib.import_module(module_name)

        errors.extend(list(_get_checks_from_module(module)))

    counts = dict(Counter(error.error_code() for error in errors))
    duplicates = {key: value for key, value in counts.items() if value > 1}

    if len(duplicates) > 0:
        raise RuntimeError(
            ("Found duplicate definitions for the following error codes: {}".format(*duplicates))
        )

    return sorted(errors, key=lambda x: (not x.terminal, x.error_code()))


def _iter_namespace(ns_pkg: ModuleType) -> Iterator[pkgutil.ModuleInfo]:
    """Iterate over the modules in a given package namespace."""
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

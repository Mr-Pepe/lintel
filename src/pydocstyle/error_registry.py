from dataclasses import dataclass
from typing import Iterable, List

from pydocstyle import DocstringError


@dataclass
class ErrorGroup:
    """A group of similarly themed errors."""

    name: str
    prefix: str


class ErrorRegistry:
    """A registry of all error codes, divided to groups."""

    def __init__(self) -> None:
        self._groups: List[ErrorGroup] = []
        self._errors: List[DocstringError] = []

    def add_group(self, group: ErrorGroup) -> None:
        self._groups.append(group)

    def add_error(self, error: DocstringError) -> None:
        self._errors.append(error)

    @property
    def groups(self) -> List[ErrorGroup]:
        return self._groups

    @property
    def errors(self) -> List[DocstringError]:
        return self._errors


error_registry = ErrorRegistry()
error_registry.add_group(ErrorGroup(name="Missing Docstrings", prefix="D1"))
error_registry.add_group(ErrorGroup(name="Whitespace Issues", prefix="D2"))
error_registry.add_group(ErrorGroup(name="Quotes Issues", prefix="D3"))
error_registry.add_group(ErrorGroup(name="Docstring Content Issues", prefix="D4"))

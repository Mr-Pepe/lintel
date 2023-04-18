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


# D4xx = ErrorRegistry.create_group('D4', 'Docstring Content Issues')
# D405 = D4xx.create_error(
#     'D405',
#     'Section name should be properly capitalized',
#     '{0!r}, not {1!r}',
# )
# D406 = D4xx.create_error(
#     'D406',
#     'Section name should end with a newline',
#     '{0!r}, not {1!r}',
# )
# D407 = D4xx.create_error(
#     'D407',
#     'Missing dashed underline after section',
#     '{0!r}',
# )
# D408 = D4xx.create_error(
#     'D408',
#     'Section underline should be in the line following the section\'s name',
#     '{0!r}',
# )
# D409 = D4xx.create_error(
#     'D409',
#     'Section underline should match the length of its name',
#     'Expected {0!r} dashes in section {1!r}, got {2!r}',
# )
# D410 = D4xx.create_error(
#     'D410',
#     'Missing blank line after section',
#     '{0!r}',
# )
# D411 = D4xx.create_error(
#     'D411',
#     'Missing blank line before section',
#     '{0!r}',
# )
# D414 = D4xx.create_error(
#     'D414',
#     'Section has no content',
#     '{0!r}',
# )
# D416 = D4xx.create_error(
#     'D416',
#     'Section name should end with a colon',
#     '{0!r}, not {1!r}',
# )
# D417 = D4xx.create_error(
#     'D417',
#     'Missing argument descriptions in the docstring',
#     'argument(s) {0} are missing descriptions in {1!r} docstring',
# )

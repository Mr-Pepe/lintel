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


# D2xx = ErrorRegistry.create_group('D2', 'Whitespace Issues')
# D200 = D2xx.create_error(
#     'D200',
#     'One-line docstring should fit on one line ' 'with quotes',
#     'found {0}',
# )
# D209 = D2xx.create_error(
#     'D209',
#     'Multi-line docstring closing quotes should be on a separate line',
# )
# D210 = D2xx.create_error(
#     'D210',
#     'No whitespaces allowed surrounding docstring text',
# )
# D212 = D2xx.create_error(
#     'D212',
#     'Multi-line docstring summary should start at the first line',
# )
# D213 = D2xx.create_error(
#     'D213',
#     'Multi-line docstring summary should start at the second line',
# )
# D214 = D2xx.create_error(
#     'D214',
#     'Section is over-indented',
#     '{0!r}',
# )
# D215 = D2xx.create_error(
#     'D215',
#     'Section underline is over-indented',
#     'in section {0!r}',
# )

# D3xx = ErrorRegistry.create_group('D3', 'Quotes Issues')
# D300 = D3xx.create_error(
#     'D300',
#     'Use """triple double quotes"""',
#     'found {0}-quotes',
# )
# D301 = D3xx.create_error(
#     'D301',
#     'Use r""" if any backslashes in a docstring',
# )
# D302 = D3xx.create_error(
#     'D302',
#     'Deprecated: Use u""" for Unicode docstrings',
# )

# D4xx = ErrorRegistry.create_group('D4', 'Docstring Content Issues')
# D402 = D4xx.create_error(
#     'D402',
#     'First line should not be the function\'s "signature"',
# )
# D404 = D4xx.create_error(
#     'D404',
#     'First word of the docstring should not be `This`',
# )
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
# D412 = D4xx.create_error(
#     'D412',
#     'No blank lines allowed between a section header and its content',
#     '{0!r}',
# )
# D413 = D4xx.create_error(
#     'D413',
#     'Missing blank line after last section',
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

# D418 = D4xx.create_error(
#     'D418',
#     'Function/ Method decorated with @overload shouldn\'t contain a docstring',
# )
# D419 = D4xx.create_error(
#     'D419',
#     'Docstring is empty',
# )


# all_errors = set(ErrorRegistry.get_error_codes())

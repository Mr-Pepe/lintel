from dataclasses import dataclass
from typing import Iterable, List

from pydocstyle.docstring_error import DocstringError


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
error_registry.add_group(
    ErrorGroup(name="Docstring Content Issues", prefix="D4")
)


# D101 = D1xx.create_error(
#     'D101',
#     'Missing docstring in public class',
# )
# D102 = D1xx.create_error(
#     'D102',
#     'Missing docstring in public method',
# )
# D103 = D1xx.create_error(
#     'D103',
#     'Missing docstring in public function',
# )
# D104 = D1xx.create_error(
#     'D104',
#     'Missing docstring in public package',
# )
# D105 = D1xx.create_error(
#     'D105',
#     'Missing docstring in magic method',
# )
# D106 = D1xx.create_error(
#     'D106',
#     'Missing docstring in public nested class',
# )
# D107 = D1xx.create_error(
#     'D107',
#     'Missing docstring in __init__',
# )

# D2xx = ErrorRegistry.create_group('D2', 'Whitespace Issues')
# D200 = D2xx.create_error(
#     'D200',
#     'One-line docstring should fit on one line ' 'with quotes',
#     'found {0}',
# )
# D201 = D2xx.create_error(
#     'D201',
#     'No blank lines allowed before function docstring',
#     'found {0}',
# )
# D202 = D2xx.create_error(
#     'D202',
#     'No blank lines allowed after function docstring',
#     'found {0}',
# )
# D203 = D2xx.create_error(
#     'D203',
#     '1 blank line required before class docstring',
#     'found {0}',
# )
# D204 = D2xx.create_error(
#     'D204',
#     '1 blank line required after class docstring',
#     'found {0}',
# )
# D205 = D2xx.create_error(
#     'D205',
#     '1 blank line required between summary line and description',
#     'found {0}',
# )
# D206 = D2xx.create_error(
#     'D206',
#     'Docstring should be indented with spaces, not tabs',
# )
# D207 = D2xx.create_error(
#     'D207',
#     'Docstring is under-indented',
# )
# D208 = D2xx.create_error(
#     'D208',
#     'Docstring is over-indented',
# )
# D209 = D2xx.create_error(
#     'D209',
#     'Multi-line docstring closing quotes should be on a separate line',
# )
# D210 = D2xx.create_error(
#     'D210',
#     'No whitespaces allowed surrounding docstring text',
# )
# D211 = D2xx.create_error(
#     'D211',
#     'No blank lines allowed before class docstring',
#     'found {0}',
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
# D400 = D4xx.create_error(
#     'D400',
#     'First line should end with a period',
#     'not {0!r}',
# )
# D401 = D4xx.create_error(
#     'D401',
#     'First line should be in imperative mood',
#     "perhaps '{0}', not '{1}'",
# )
# D401b = D4xx.create_error(
#     'D401',
#     'First line should be in imperative mood; try rephrasing',
#     "found '{0}'",
# )
# D402 = D4xx.create_error(
#     'D402',
#     'First line should not be the function\'s "signature"',
# )
# D403 = D4xx.create_error(
#     'D403',
#     'First word of the first line should be properly capitalized',
#     '{0!r}, not {1!r}',
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
# D415 = D4xx.create_error(
#     'D415',
#     (
#         'First line should end with a period, question '
#         'mark, or exclamation point'
#     ),
#     'not {0!r}',
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

"""General shared utilities."""
import re
from itertools import tee, zip_longest
from typing import Any, Iterable, List, Tuple, TypeVar

from pydocstyle.parser import Definition

#: Regular expression for stripping non-alphanumeric characters
NON_ALPHANUMERIC_STRIP_RE = re.compile(r'[\W_]+')

T = TypeVar("T")


def is_blank(string: str) -> bool:
    """Return True iff the string contains only whitespaces."""
    return not string.strip()


def has_content(string: str) -> bool:
    """Return True iff the string does not contain only whitespaces."""
    return not is_blank(string)


def pairwise(
    iterable: Iterable[T],
    default_value: T,
) -> Iterable[Tuple[T, T]]:
    """Return pairs of items from `iterable`.

    pairwise([1, 2, 3], default_value=None) -> (1, 2) (2, 3), (3, None)
    """
    a, b = tee(iterable)
    _ = next(b, default_value)
    return zip_longest(a, b, fillvalue=default_value)


def common_prefix_length(a: str, b: str) -> int:
    """Return the length of the longest common prefix of a and b.

    >>> common_prefix_length('abcd', 'abce')
    3

    """
    for common, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            return common
    return min(len(a), len(b))


def strip_non_alphanumeric(string: str) -> str:
    """Strip string from any non-alphanumeric characters."""
    return NON_ALPHANUMERIC_STRIP_RE.sub('', string)


def leading_space(string: str) -> str:
    """Return any leading space from `string`."""
    match = re.compile(r'\s*').match(string)

    assert match

    return match.group()


def get_indents(
    definition: Definition, docstring: str
) -> Tuple[str, List[str]]:
    """Return the indentation of docstring quotes and content lines."""
    before_docstring, _, _ = definition.source.partition(docstring)
    _, _, docstring_indent = before_docstring.rpartition('\n')

    lines = [
        next_line
        for first_line, next_line in pairwise(docstring.split("\n"), "")
        if has_content(next_line) and not first_line.endswith('\\')
    ]

    line_indents = [leading_space(l) for l in lines]

    return docstring_indent, line_indents

"""General shared utilities."""
import re
from itertools import tee, zip_longest
from typing import Any, Iterable, List, Tuple, TypeVar, Union

import astroid
from astroid import NodeNG

from pydocstyle.docstring import Docstring

CHECKED_NODE_TYPE = Union[
    astroid.ClassDef, astroid.FunctionDef, astroid.Module
]
NODES_TO_CHECK = (astroid.ClassDef, astroid.FunctionDef, astroid.Module)


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
    node: CHECKED_NODE_TYPE, docstring: Docstring
) -> Tuple[str, List[str]]:
    """Return the indentation of docstring quotes and content lines."""
    before_docstring, _, _ = node.as_string().partition(docstring.doc)
    _, _, docstring_indent = before_docstring.rpartition('\n')

    lines = [
        next_line
        for first_line, next_line in pairwise(docstring.doc.split("\n"), "")
        if has_content(next_line) and not first_line.endswith('\\')
    ]

    line_indents = [leading_space(l) for l in lines]

    return docstring_indent, line_indents


def source_has_noqa(source: str) -> bool:
    """Return whether the source code contains a `# pydoclint: noqa` comment.

    Any number of whitespaces is allowed between the hashtag, `pydoclint`, `:`, and `noqa`
    but nothing else can be on that line.
    """
    regex = re.compile(r"^\s*#\s*pydoclint\s*:\s*noqa\s*$")
    for line in source.splitlines():
        if regex.search(line):
            return True

    return False


def get_line_noqa(line: str) -> list[str]:
    ignore_all_regex = re.compile(r".*#\s*noqa(\s*$|\s*#)")
    if ignore_all_regex.search(line):
        return ["all"]

    return []


def get_decorator_names(node: NodeNG) -> list[str]:
    decorator_names: list[str] = []

    decorators = [
        child_node
        for child_node in node.get_children()
        if isinstance(child_node, astroid.Decorators)
    ]

    if decorators:
        for decorator in decorators[0].nodes:
            if isinstance(decorator, astroid.Name):
                decorator_names.append(decorator.name)
            if isinstance(decorator, astroid.Call):
                decorator_names.append(decorator.func.name)

    return decorator_names


def is_public(node: CHECKED_NODE_TYPE) -> bool:
    if is_dunder(node):
        return True

    if node.name.startswith("_"):
        return False

    if (
        isinstance(node.parent, astroid.Module)
        and not node.name in node.parent.wildcard_import_names()
    ):
        return False

    while node.parent is not None:
        if not is_public(node.parent):
            return False

        node = node.parent

    return True


def is_private(node: CHECKED_NODE_TYPE) -> bool:
    return not is_public(node)


def is_dunder(node: CHECKED_NODE_TYPE) -> bool:
    return node.name.startswith('__') and node.name.endswith('__')

"""General shared utilities."""

import re
from itertools import tee, zip_longest
from typing import Iterable, List, Set, Tuple, TypeVar

import astroid
from astroid import ClassDef, FunctionDef, Module

from lintel import CHECKED_NODE_TYPES

#: Regular expression for stripping non-alphanumeric characters
NON_ALPHANUMERIC_STRIP_RE = re.compile(r'[\W_]+')

VARIADIC_MAGIC_METHODS = ("__new__", "__init__", "__call__")

T = TypeVar("T")

__all__ = (
    "VARIADIC_MAGIC_METHODS",
    "is_blank",
    "has_content",
    "pairwise",
    "common_prefix_length",
    "strip_non_alphanumeric",
    "leading_space",
    "get_decorator_names",
    "is_public",
    "is_private",
    "is_dunder",
    "is_overloaded",
    "is_nested_class",
)


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


def get_decorator_names(node: CHECKED_NODE_TYPES) -> List[str]:
    """Return the decorator names applied to a node."""
    decorator_names: List[str] = []

    decorators = [
        child_node
        for child_node in node.get_children()
        if isinstance(child_node, astroid.Decorators)
    ]

    if decorators:
        for decorator in decorators[0].nodes:
            if isinstance(decorator, astroid.Name):
                decorator_names.append(decorator.name)
            if isinstance(decorator, astroid.Call) and decorator.func:
                if hasattr(decorator.func, "name"):
                    decorator_names.append(decorator.func.name)
                elif hasattr(decorator.func, "attrname"):
                    decorator_names.append(decorator.func.attrname)

    return decorator_names


def is_public(node: CHECKED_NODE_TYPES) -> bool:
    """Return whether a node is public."""
    if is_dunder(node):
        return True

    if node.name.startswith("_"):
        return False

    if (
        isinstance(node.parent, astroid.Module)
        and not node.name in node.parent.wildcard_import_names()
    ):
        return False

    if isinstance(node, astroid.ClassDef) and isinstance(node.parent, astroid.FunctionDef):
        # Classes are not considered public if nested in a function
        return False

    while node.parent is not None:
        if not is_public(node.parent):
            return False

        node = node.parent

    return True


def is_private(node: CHECKED_NODE_TYPES) -> bool:
    """Return whether a node is private."""
    return not is_public(node)


def is_dunder(node: CHECKED_NODE_TYPES) -> bool:
    """Return whether a node has a '__dunder__' name."""
    return node.name.startswith('__') and node.name.endswith('__')


def is_overloaded(function_: FunctionDef) -> bool:
    """Return whether the function has an ``overload`` decorator."""
    return "overload" in get_decorator_names(function_)


def is_nested_class(class_: ClassDef) -> bool:
    """Return whether the class is nested in a function or class."""
    return isinstance(class_.parent, (FunctionDef, ClassDef))

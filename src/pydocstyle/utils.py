"""General shared utilities."""

import re
from itertools import tee, zip_longest
from typing import Iterable, List, Set, Tuple, TypeVar, Union

import astroid
from astroid import ClassDef, FunctionDef, Module

CHECKED_NODE_TYPE = Union[
    astroid.ClassDef, astroid.FunctionDef, astroid.Module
]
NODES_TO_CHECK = (astroid.ClassDef, astroid.FunctionDef, astroid.Module)


#: Regular expression for stripping non-alphanumeric characters
NON_ALPHANUMERIC_STRIP_RE = re.compile(r'[\W_]+')

VARIADIC_MAGIC_METHODS = ("__new__", "__init__", "__call__")

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


def get_error_codes_to_skip(node: CHECKED_NODE_TYPE) -> Set[str]:
    """Return the error codes to skip for the given node.

    {"all"} will be returned if all error codes should be skipped.
    """
    error_codes_to_skip: Set[str] = set()

    # Check for blank ignore in module
    if isinstance(node, Module):
        ignore_all_regex = re.compile(r"^\s*#\s*pydoclint\s*:\s*noqa\s*$")
        specific_ignore_regex = re.compile(r"^\s*#\s*noqa\s*:[\sA-Z\d,]*D\d+")

        for line in node.file_bytes.decode().splitlines():
            if ignore_all_regex.search(line):
                return {"all"}

            for match in specific_ignore_regex.findall(line):
                for error_code in re.findall(r"D\d{0,3}\b", match):
                    error_codes_to_skip.add(error_code)

    # Check for inline ignores
    if isinstance(node, (FunctionDef, ClassDef)):
        return _get_line_noqa(_get_definition_line(node))

    return error_codes_to_skip


def _get_line_noqa(line: str) -> Set[str]:
    ignore_all_regex = re.compile(r".*#\s*noqa(\s*$|\s*#)")
    specific_ignore_regex = re.compile(r".*#\s*noqa\s*:\s*([\sA-Z\d,]*D\d+)")

    if ignore_all_regex.search(line):
        return {"all"}

    error_codes_to_skip: Set[str] = set()

    for match in specific_ignore_regex.findall(line):
        for error_code in re.findall(r"D\d{0,3}\b", match):
            error_codes_to_skip.add(error_code)

    return error_codes_to_skip


def _get_definition_line(node: Union[FunctionDef, ClassDef]) -> str:
    lines = (
        node.root()
        .file_bytes.decode()
        .splitlines()[node.lineno - 1 : node.end_lineno]
    )
    for line in lines:
        if line.lstrip().startswith(("def", "async def", "class")):
            return line

    raise ValueError(f"'{node.name}' does not contain a definition line.")


def get_decorator_names(node: CHECKED_NODE_TYPE) -> List[str]:
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


def is_public(node: CHECKED_NODE_TYPE) -> bool:
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

    if isinstance(node, astroid.ClassDef) and isinstance(
        node.parent, astroid.FunctionDef
    ):
        # Classes are not considered public if nested in a function
        return False

    while node.parent is not None:
        if not is_public(node.parent):
            return False

        node = node.parent

    return True


def is_private(node: CHECKED_NODE_TYPE) -> bool:
    """Return whether a node is private."""
    return not is_public(node)


def is_dunder(node: CHECKED_NODE_TYPE) -> bool:
    """Return whether a node has a '__dunder__' name."""
    return node.name.startswith('__') and node.name.endswith('__')


def is_overloaded(function_: FunctionDef) -> bool:
    """Return whether the function has an ``overload`` decorator."""
    return "overload" in get_decorator_names(function_)


def get_leading_words(line: str) -> str:
    """Return any leading set of words from `line`.

    For example, if `line` is "  Hello world!!!", returns "Hello world".
    """
    result = re.compile(r"[\w ]+").match(line.strip())
    if result is not None:
        return result.group()

    return ""


def is_ascii(string: str) -> bool:
    """Return a boolean indicating if `string` only has ascii characters."""
    return all(ord(char) < 128 for char in string)

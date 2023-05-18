from typing import List, Set

import astroid
import pytest

from lintel import Configuration, _utils

__all__ = ()


def test_common_prefix():
    """Test common prefix length of two strings."""
    assert _utils.common_prefix_length('abcd', 'abce') == 3


def test_no_common_prefix():
    """Test common prefix length of two strings that have no common prefix."""
    assert _utils.common_prefix_length('abcd', 'cdef') == 0


def test_differ_length():
    """Test common prefix length of two strings differing in length."""
    assert _utils.common_prefix_length('abcd', 'ab') == 2


def test_empty_string():
    """Test common prefix length of two strings, one of them empty."""
    assert _utils.common_prefix_length('abcd', '') == 0


def test_strip_non_alphanumeric():
    """Test strip of a string leaves only alphanumeric characters."""
    assert _utils.strip_non_alphanumeric("  1abcd1...") == "1abcd1"


@pytest.mark.parametrize(
    ("code", "expected_decorators"),
    [
        ("def func():\n\t...", []),
        ("@my_decorator\ndef func():\n\t...", ["my_decorator"]),
        (
            "@my_decorator\n@my_second_decorator\ndef func():\n\t...",
            ["my_decorator", "my_second_decorator"],
        ),
        (
            "@my_decorator('a')\n@my_second_decorator\ndef func():\n\t...",
            ["my_decorator", "my_second_decorator"],
        ),
        (
            "def my_decorator(a):\n\t...\n@my_decorator\ndef func():\n\t...",
            ["my_decorator"],
        ),
    ],
)
def test_get_decorator_names(code: str, expected_decorators: Set[str]) -> None:
    node = list(f for f in astroid.parse(code).get_children() if f.name == "func")[0]
    assert isinstance(node, astroid.FunctionDef)
    assert _utils.get_decorator_names(node) == expected_decorators

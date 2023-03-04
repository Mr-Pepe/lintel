from typing import Set

import astroid
import pytest

from pydocstyle import utils

__all__ = ()


def test_common_prefix():
    """Test common prefix length of two strings."""
    assert utils.common_prefix_length('abcd', 'abce') == 3


def test_no_common_prefix():
    """Test common prefix length of two strings that have no common prefix."""
    assert utils.common_prefix_length('abcd', 'cdef') == 0


def test_differ_length():
    """Test common prefix length of two strings differing in length."""
    assert utils.common_prefix_length('abcd', 'ab') == 2


def test_empty_string():
    """Test common prefix length of two strings, one of them empty."""
    assert utils.common_prefix_length('abcd', '') == 0


def test_strip_non_alphanumeric():
    """Test strip of a string leaves only alphanumeric characters."""
    assert utils.strip_non_alphanumeric("  1abcd1...") == "1abcd1"


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("# pydoclint: noqa", {"all"}),
        ("#pydoclint:noqa", {"all"}),
        ("#   pydoclint   :   noqa   ", {"all"}),
        ("a = 1\n#pydoclint:noqa\n# Some more text", {"all"}),
        ("# noqa: D100", {"D100"}),
        ("# noqa: A123,D1234,D1,D100,D300", {"D1", "D100", "D300"}),
        (
            "def my_func(): # noqa: D1,D100,D300\n\t...",
            set(),
        ),
        ("# Some text\n#pydoclint:noq\n# Some more text", set()),
        ("# pydoclint: noqa # And something else", set()),
        ("# And something else # pydoclint: noqa", set()),
        ("", set()),
        ("# noqa", set()),
        ("#noqa", set()),
        ("#pydoclint", set()),
    ],
)
def test_error_codes_to_skip_module(source: str, expected: bool) -> None:
    node = astroid.parse(source)
    assert utils.get_error_codes_to_skip(node) == expected


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (
            "def my_func(): # noqa\n\t...",
            {"all"},
        ),
        (
            "def my_func():    #   noqa # and more\n\t...",
            {"all"},
        ),
        (
            "def my_func():    #   noqa: E501,D100,D200 # and more\n\t...",
            {"D100", "D200"},
        ),
    ],
)
def test_error_codes_to_skip_class_and_function(
    source: str, expected: bool
) -> None:
    node = next(astroid.parse(source).get_children())
    assert utils.get_error_codes_to_skip(node) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("def func(): # noqa", {"all"}),
        ("def func(): #   noqa   ", {"all"}),
        ("def func(): #   noqa  # Another comment", {"all"}),
        ("def func(): # Another comment #   noqa", {"all"}),
        ("def func(): # Another comment #   noqa something", set()),
    ],
)
def test_get_line_noqa(line: str, expected: list[str]) -> None:
    assert utils._get_line_noqa(line) == expected


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
    node = list(
        f for f in astroid.parse(code).get_children() if f.name == "func"
    )[0]
    assert isinstance(node, astroid.FunctionDef)
    assert utils.get_decorator_names(node) == expected_decorators

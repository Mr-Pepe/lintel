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
        ("# pydoclint: noqa", True),
        ("#pydoclint:noqa", True),
        ("#   pydoclint   :   noqa   ", True),
        ("Some text\n#pydoclint:noqa\nSome more text", True),
        ("Some text\n#pydoclint:noq\nSome more text", False),
        ("# pydoclint: noqa # And something else", False),
        ("# And something else # pydoclint: noqa", False),
        ("", False),
        ("# noqa", False),
        ("#noqa", False),
        ("pydoclint", False),
        ("noqa", False),
    ],
)
def test_source_has_noqa(source: str, expected: bool) -> None:
    assert utils.source_has_noqa(source) is expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("def func(): # noqa", ["all"]),
        ("def func(): #   noqa   ", ["all"]),
        ("def func(): #   noqa  # Another comment", ["all"]),
        ("def func(): # Another comment #   noqa", ["all"]),
        ("def func(): # Another comment #   noqa something", []),
    ],
)
def test_get_line_noqa(line: str, expected: list[str]) -> None:
    assert utils.get_line_noqa(line) == expected


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
def test_get_decorator_names(
    code: str, expected_decorators: list[str]
) -> None:
    node = list(
        f for f in astroid.parse(code).get_children() if f.name == "func"
    )[0]
    assert isinstance(node, astroid.FunctionDef)
    assert utils.get_decorator_names(node) == expected_decorators

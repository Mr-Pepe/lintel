from typing import List

import astroid
import pytest

from lintel import (
    CONVENTION_ERRORS,
    Configuration,
    Convention,
    get_all_error_codes,
    get_error_codes,
    get_error_codes_to_skip,
    get_line_noqa,
)


def test_error_codes_of_conventions() -> None:
    assert get_error_codes(Configuration(convention=Convention.NONE)) == set()
    assert get_error_codes(Configuration(convention=Convention.ALL)) == get_all_error_codes()

    # Make sure that all error codes from the conventions are shipped by default
    assert (
        get_error_codes(Configuration(convention=Convention.DEFAULT))
        == CONVENTION_ERRORS[Convention.DEFAULT]
    )
    assert (
        get_error_codes(Configuration(convention=Convention.NUMPY))
        == CONVENTION_ERRORS[Convention.NUMPY]
    )
    assert (
        get_error_codes(Configuration(convention=Convention.GOOGLE))
        == CONVENTION_ERRORS[Convention.GOOGLE]
    )


def test_raises_error_if_specified_error_is_not_registered() -> None:
    config = Configuration(convention=Convention.NONE, select={"D1234567890"})

    with pytest.raises(
        ValueError,
        match="Error code 'D1234567890' is selected explicitly or by the convention 'none' but no "
        "check is registered for it.",
    ):
        get_error_codes(config)


def test_error_codes_are_added() -> None:
    config = Configuration(convention=Convention.NONE, select={"D100"})

    assert get_error_codes(config) == {"D100"}


def test_error_codes_are_removed() -> None:
    config = Configuration(convention=Convention.ALL, ignore={"D100"})

    error_codes = get_error_codes(config)

    assert len(error_codes) == len(get_all_error_codes()) - 1
    assert "D100" not in error_codes


def test_ignore_takes_precedence_over_select() -> None:
    config = Configuration(convention=Convention.NONE, select={"D100"}, ignore={"D100"})

    assert get_error_codes(config) == set()


def test_raises_error_if_ignored_error_code_has_no_check() -> None:
    config = Configuration(convention=Convention.NONE, ignore={"D1234567890"})

    with pytest.raises(
        ValueError,
        match="Error code 'D1234567890' is unnecessarily ignored. No such check is registered.",
    ):
        assert get_error_codes(config) == set()


def test_ignoring_unselected_error_does_not_crash() -> None:
    config = Configuration(convention=Convention.NONE, ignore={"D100"})

    assert get_error_codes(config) == set()


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("# lintel: noqa", get_all_error_codes()),
        ("#lintel:noqa", get_all_error_codes()),
        ("#   lintel   :   noqa   ", get_all_error_codes()),
        ("a = 1\n#lintel:noqa\n# Some more text", get_all_error_codes()),
        ("# noqa: D100", {"D100"}),
        ("# noqa: A123,D1234,D1,D100,D300", {"D1", "D100", "D300"}),
        (
            "def my_func(): # noqa: D1,D100,D300\n\t...",
            set(),
        ),
        ("# Some text\n#lintel:noq\n# Some more text", set()),
        ("# lintel: noqa # And something else", set()),
        ("# And something else # lintel: noqa", set()),
        ("", set()),
        ("# noqa", set()),
        ("#noqa", set()),
        ("#lintel", set()),
    ],
)
def test_error_codes_to_skip_module(source: str, expected: bool) -> None:
    node = astroid.parse(source)
    assert get_error_codes_to_skip(node, False) == expected


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (
            "def my_func(): # noqa\n\t...",
            get_all_error_codes(),
        ),
        (
            "def my_func():    #   noqa # and more\n\t...",
            get_all_error_codes(),
        ),
        (
            "def my_func():    #   noqa: E501,D100,D200 # and more\n\t...",
            {"D100", "D200"},
        ),
    ],
)
def test_error_codes_to_skip_class_and_function(source: str, expected: bool) -> None:
    node = next(astroid.parse(source).get_children())
    assert get_error_codes_to_skip(node) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("def func(): # noqa", get_all_error_codes()),
        ("def func(): #   noqa   ", get_all_error_codes()),
        ("def func(): #   noqa  # Another comment", get_all_error_codes()),
        ("def func(): # Another comment #   noqa", get_all_error_codes()),
        ("def func(): # Another comment #   noqa something", set()),
    ],
)
def test_get_line_noqa(line: str, expected: List[str]) -> None:
    assert get_line_noqa(line) == expected

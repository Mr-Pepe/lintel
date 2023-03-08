"""Tests for the violations.Error class."""

import collections
import textwrap
from pathlib import Path

import astroid
import pytest

from pydocstyle.violations import Error


class MockDefinition:
    def __init__(self, source: str) -> None:
        self.source = source

    def as_string(self) -> str:
        return self.source


def test_message_without_context():
    """Test a simple error message without parameters."""
    error = Error('CODE', 'an error', None)
    assert error.message == 'CODE: an error'


def test_message_with_context():
    """Test an error message with parameters."""
    error = Error('CODE', 'an error', 'got {}', 0)
    assert error.message == 'CODE: an error (got 0)'


def test_message_with_insufficient_parameters():
    """Test an error message with invalid parameter invocation."""
    error = Error('CODE', 'an error', 'got {}')
    with pytest.raises(IndexError):
        assert error.message


def test_lines(tmp_path: Path):
    """Test proper printing of source lines, including blank line trimming."""
    test_file_path = tmp_path / "test.py"

    with open(test_file_path, mode="w", encoding="utf-8") as file:
        file.write(
            textwrap.dedent(
                '''



                def foo():
                    """A docstring."""

                    pass
            '''
            )
        )

    with open(test_file_path, mode="r", encoding="utf-8") as file:
        node = list(
            astroid.parse(
                file.read(), module_name="test", path=str(test_file_path)
            ).get_children()
        )[0]

    error = Error('CODE', 'an error', None)
    error.set_context(node, None)
    print(error.lines)
    assert error.lines == textwrap.dedent(
        '''\
        5: def foo():
        6:     """A docstring."""
        7:
        8:     pass
    '''
    )

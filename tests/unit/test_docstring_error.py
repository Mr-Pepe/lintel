"""Tests for the violations.Error class."""


import os

import astroid
import pytest

from lintel import Configuration, DocstringError, get_docstring_from_doc_node

FUNCTION_CODE = """def my_func() -> None:
        ...
    """

CLASS_CODE = '''class MyClass:
        """Docstring."""
        ...
    '''

module_path = os.path.normcase(os.path.abspath("/path/to/my/file"))

module_node = astroid.parse(
    code=f"\n{FUNCTION_CODE}\n\n{CLASS_CODE}",
    module_name="my_module",
    path=module_path,
)

function_node = list(module_node.get_children())[0]
class_node = list(module_node.get_children())[1]


class D123(DocstringError):
    description = "some short description"


def test_file_name() -> None:
    error = D123(module_node)

    assert error.file_name == str(module_path)


def test_line() -> None:
    error = D123(function_node)

    assert error.line == 2


def test_node_name() -> None:
    error = D123(function_node)

    assert error.node_name == "my_func"


def test_print_for_function_node() -> None:
    error = D123(function_node)

    assert str(error) == f"{module_path}:2 in function 'my_func' -> D123: some short description"


def test_print_for_module_node() -> None:
    error = D123(module_node)

    assert str(error) == f"{module_path}:0 in module 'my_module' -> D123: some short description"


def test_print_for_class_node() -> None:
    error = D123(class_node)

    assert str(error) == f"{module_path}:6 in class 'MyClass' -> D123: some short description"


def test_str_and_repr() -> None:
    error = D123(class_node)

    assert str(error) == error.__repr__()


def test_unimplemented_error_is_raised_if_check_is_missing() -> None:
    error = D123(class_node)

    with pytest.raises(NotImplementedError):
        error.check_implementation(
            class_node,
            get_docstring_from_doc_node(class_node, Configuration()),
            Configuration(),
        )

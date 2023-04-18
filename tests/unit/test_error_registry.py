from pydocstyle import DocstringError
from pydocstyle.error_registry import ErrorGroup, ErrorRegistry


class MyError(DocstringError):
    error_code = "D123"
    description = "some short description"


def test_add_group() -> None:
    registry = ErrorRegistry()

    assert len(registry.groups) == 0

    group = ErrorGroup(name="My group", prefix="D1")

    registry.add_group(group)

    assert len(registry.groups) == 1
    assert registry.groups[0] == group


def test_add_error() -> None:
    registry = ErrorRegistry()

    assert len(registry.errors) == 0

    registry.add_error(MyError)

    assert len(registry.errors) == 1
    assert registry.errors[0] == MyError

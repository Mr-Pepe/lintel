"""Contains checks for proper punctuation at the end of the first line."""

from typing import Callable, Optional, Tuple, Type, TypeVar, Union

from astroid import NodeNG

from lintel import CHECKED_NODE_TYPES, Configuration, Docstring, DocstringError


class D400(DocstringError):
    description = "First line should end with a period (not {!r})."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D400"]:
        return _check_ends_with(node, docstring, '.', cls)


class D415(DocstringError):
    description = (
        "First line should end with a period, question mark, or exclamation point (not {!r})."
    )

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D415"]:
        return _check_ends_with(node, docstring, ('.', '!', '?'), cls)


T = TypeVar("T", bound=DocstringError)


def _check_ends_with(
    node: CHECKED_NODE_TYPES,
    docstring: Docstring,
    chars: Union[str, Tuple[str, ...]],
    error_class: Type[T],
) -> Optional[T]:
    """Raise error of type `error_class` if first line of docstring does not end with `chars`."""
    summary_line: str = docstring.content.strip().split('\n')[0]

    if not summary_line.endswith(chars):
        error = error_class(node)
        error.parameters = [summary_line[-1]]

        return error

    return None

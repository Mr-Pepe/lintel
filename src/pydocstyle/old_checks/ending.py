"""Contains checks for proper punctuation at the end of the first line."""

from typing import Callable, Optional, Tuple, Union

from astroid import NodeNG

from pydocstyle._config import Configuration
from pydocstyle._docstring import Docstring
from pydocstyle._docstring_error import D400, D415, Error
from pydocstyle.checks import check


@check(NodeNG)
def check_ends_with_period(_: NodeNG, docstring: Docstring, __: Configuration) -> Optional[D400]:
    """D400: First line should end with a period."""
    return _check_ends_with(docstring, '.', D400)


@check(NodeNG)
def check_ends_with_punctuation(
    _: NodeNG, docstring: Docstring, __: Configuration
) -> Optional[D415]:
    """D415: Should end with period, question mark, or exclamation point."""
    return _check_ends_with(docstring, ('.', '!', '?'), D415)


def _check_ends_with(
    docstring: Docstring,
    chars: Union[str, Tuple[str, ...]],
    violation: Callable[..., Error],
) -> Optional[Callable[..., Error]]:
    """Raise `violation` if first line of docstring does not end with `chars`."""
    if not docstring:
        return None

    summary_line: str = docstring.content.strip().split('\n')[0]

    if summary_line.endswith(chars):
        return None

    return violation(summary_line[-1])

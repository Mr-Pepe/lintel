import ast
from typing import Callable, Optional, Tuple, Union

from pydocstyle.checks import check
from pydocstyle.parser import Definition
from pydocstyle.violations import D400, D415, Error


@check(Definition)
def check_ends_with_period(_: Definition, docstring: str) -> Optional[D400]:
    """D400: First line should end with a period."""
    return _check_ends_with(docstring, '.', D400)


@check(Definition)
def check_ends_with_punctuation(
    _: Definition, docstring: str
) -> Optional[D415]:
    """D415: Should end with period, question mark, or exclamation point."""
    return _check_ends_with(docstring, ('.', '!', '?'), D415)


def _check_ends_with(
    docstring: str,
    chars: Union[str, Tuple[str, ...]],
    violation: Callable[..., Error],
) -> Optional[Callable[..., Error]]:
    """Raise `violation` if first line of docstring does not end with `chars`."""
    if not docstring:
        return None

    summary_line: str = ast.literal_eval(docstring).strip().split('\n')[0]

    if summary_line.endswith(chars):
        return None

    return violation(summary_line[-1])

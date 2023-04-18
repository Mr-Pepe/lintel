"""Contains a check whether a docstring starts with `This`."""

from typing import Optional

from astroid import NodeNG

from pydocstyle._config import Configuration
from pydocstyle._docstring import Docstring
from pydocstyle._docstring_error import D404
from pydocstyle._utils import strip_non_alphanumeric
from pydocstyle.checks import check


@check(NodeNG)
def check_starts_with_this(_: NodeNG, docstring: Docstring, __: Configuration) -> Optional[D404]:
    """D404: First word of the docstring should not be `This`.

    Docstrings should use short, simple language. They should not begin
    with "This class is [..]" or "This module contains [..]".
    """
    stripped = docstring.content.strip()

    if not stripped:
        return None

    first_word = strip_non_alphanumeric(stripped.split()[0])

    if first_word.lower() != 'this':
        return None

    return D404()

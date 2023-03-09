import ast
from typing import Optional

from astroid import NodeNG

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import strip_non_alphanumeric
from pydocstyle.violations import D404


@check(NodeNG)
def check_starts_with_this(
    _: NodeNG, docstring: Docstring, __: Configuration
) -> Optional[D404]:
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

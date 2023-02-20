import ast
from typing import Optional

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.parser import Definition
from pydocstyle.utils import strip_non_alphanumeric
from pydocstyle.violations import D404


@check(Definition)
def check_starts_with_this(
    _: Definition, docstring: str, __: Configuration
) -> Optional[D404]:
    """D404: First word of the docstring should not be `This`.

    Docstrings should use short, simple language. They should not begin
    with "This class is [..]" or "This module contains [..]".
    """
    if not docstring:
        return None

    stripped = ast.literal_eval(docstring).strip()

    if not stripped:
        return None

    first_word = strip_non_alphanumeric(stripped.split()[0])

    if first_word.lower() != 'this':
        return None

    return D404()

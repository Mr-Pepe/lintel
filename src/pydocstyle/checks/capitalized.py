import ast
import string
from typing import Optional

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.parser import Function
from pydocstyle.violations import D403


@check(Function)
def check_capitalized(
    _: Function, docstring: str, __: Configuration
) -> Optional[D403]:
    """D403: First word of the first line should be properly capitalized."""
    if not docstring:
        return None

    first_word: str = ast.literal_eval(docstring).split()[0]

    if first_word in (first_word.upper(), first_word.capitalize()):
        return None

    for char in first_word:
        if char not in string.ascii_letters and char != "'":
            return None

    return D403(first_word.capitalize(), first_word)

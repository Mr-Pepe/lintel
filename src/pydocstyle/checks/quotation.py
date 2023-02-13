import ast
import re
from typing import Optional

from pydocstyle.checks import check
from pydocstyle.parser import Definition
from pydocstyle.violations import D300


@check(Definition)
def check_triple_double_quotes(
    _: Definition, docstring: str
) -> Optional[D300]:
    r'''D300: Use """triple double quotes""".

    For consistency, always use """triple double quotes""" around
    docstrings. Use r"""raw triple double quotes""" if you use any
    backslashes in your docstrings.

    Note: Exception to this is made if the docstring contains
        """ quotes in its body.
    '''
    if not docstring:
        return None

    if '"""' in ast.literal_eval(docstring):
        # Allow ''' quotes if docstring contains """, because
        # otherwise """ quotes could not be expressed inside
        # docstring. Not in PEP 257.
        regex = re.compile(r"[uU]?[rR]?'''[^'].*")
    else:
        regex = re.compile(r'[uU]?[rR]?"""[^"].*')

    if regex.match(docstring):
        return None

    illegal_match = re.compile(r"""[uU]?[rR]?("+|'+).*""").match(docstring)
    assert illegal_match is not None

    illegal_quotes = illegal_match.group(1)

    return D300(illegal_quotes)

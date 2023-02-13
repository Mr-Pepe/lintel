import ast
import re
from typing import Optional

from pydocstyle.checks import check
from pydocstyle.parser import Definition
from pydocstyle.violations import D300, D301


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


@check(Definition)
def check_backslashes(_: Definition, docstring: str) -> Optional[D301]:
    r'''D301: Use r""" if any backslashes in a docstring.

    Use r"""raw triple double quotes""" if you use any backslashes
    (\) in your docstrings.

    Exceptions are backslashes for line-continuation and unicode escape
    sequences \N... and \u... These are considered intended unescaped
    content in docstrings.
    '''
    # Just check that docstring is raw, check_triple_double_quotes
    # ensures the correct quotes.
    if not docstring:
        return None

    if not re.compile(r'\\[^\nuN]').search(docstring):
        # No backslash in docstring
        return None

    if docstring.startswith(('r', 'ur')):
        return None

    return D301()

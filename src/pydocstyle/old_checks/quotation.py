"""Contains checks for proper docstring quotation."""

import re
from typing import Optional

from pydocstyle._config import Configuration
from pydocstyle._docstring import Docstring
from pydocstyle._docstring_error import D300, D301
from pydocstyle._utils import CHECKED_NODE_TYPES, NODES_TO_CHECK
from pydocstyle.checks import check


@check(NODES_TO_CHECK)
def check_triple_double_quotes(
    _: CHECKED_NODE_TYPES, docstring: Docstring, __: Configuration
) -> Optional[D300]:
    r'''D300: Use """triple double quotes""".

    For consistency, always use """triple double quotes""" around
    docstrings. Use r"""raw triple double quotes""" if you use any
    backslashes in your docstrings.

    Note: Exception to this is made if the docstring contains
        """ quotes in its body.
    '''
    if '"""' in docstring.content:
        # Allow ''' quotes if docstring contains """, because
        # otherwise """ quotes could not be expressed inside
        # docstring. Not in PEP 257.
        regex = re.compile(r".*?[uU]?[rR]?[^']'''[^'].*")
    else:
        regex = re.compile(r'.*?[uU]?[rR]?([^"]|^)"""[^"\n].*')

    if regex.match(docstring.raw):
        return None

    illegal_match = re.compile(r""".*?[uU]?[rR]?("+|'+).*""").match(docstring.raw)
    assert illegal_match is not None

    illegal_quotes = illegal_match.group(1)

    if illegal_quotes == '"""':
        return None

    return D300(illegal_quotes)


@check(NODES_TO_CHECK)
def check_backslashes(
    _: CHECKED_NODE_TYPES, docstring: Docstring, __: Configuration
) -> Optional[D301]:
    r'''D301: Use r""" if any backslashes in a docstring.

    Use r"""raw triple double quotes""" if you use any backslashes
    (\) in your docstrings.

    Exceptions are backslashes for line-continuation and unicode escape
    sequences \N... and \u... These are considered intended unescaped
    content in docstrings.
    '''
    # Just check that docstring is raw, check_triple_double_quotes
    # ensures the correct quotes.
    if not re.compile(r'\\[^\nuN]').search(docstring.content):
        # No backslash in docstring
        return None

    if docstring.raw.strip().startswith(('r', 'ur')):
        return None

    return D301()

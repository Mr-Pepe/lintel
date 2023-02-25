import linecache
import re
from typing import Optional

from astroid import NodeNG

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import CHECKED_NODE_TYPE, NODES_TO_CHECK
from pydocstyle.violations import D300, D301


@check(NODES_TO_CHECK)
def check_triple_double_quotes(
    node: CHECKED_NODE_TYPE, docstring: Docstring, config: Configuration
) -> Optional[D300]:
    r'''D300: Use """triple double quotes""".

    For consistency, always use """triple double quotes""" around
    docstrings. Use r"""raw triple double quotes""" if you use any
    backslashes in your docstrings.

    Note: Exception to this is made if the docstring contains
        """ quotes in its body.
    '''
    raw_docstring = "".join(
        l.strip()
        for l in linecache.getlines(node.root().file)[
            node.doc_node.fromlineno - 1 : node.doc_node.end_lineno
        ]
    )

    if '"""' in docstring.doc:
        # Allow ''' quotes if docstring contains """, because
        # otherwise """ quotes could not be expressed inside
        # docstring. Not in PEP 257.
        regex = re.compile(r"[uU]?[rR]?'''[^'].*")
    else:
        regex = re.compile(r'[uU]?[rR]?"""[^"].*')

    if regex.match(raw_docstring):
        return None

    illegal_match = re.compile(r"""[uU]?[rR]?("+|'+).*""").match(raw_docstring)
    assert illegal_match is not None

    illegal_quotes = illegal_match.group(1)

    return D300(illegal_quotes)


@check(NodeNG)
def check_backslashes(
    _: NodeNG, docstring: Docstring, config: Configuration
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
    if not re.compile(r'\\[^\nuN]').search(docstring.doc):
        # No backslash in docstring
        return None

    if docstring.startswith(('r', 'ur')):
        return None

    return D301()

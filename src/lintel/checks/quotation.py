"""Contains checks for proper docstring quotation."""

import re
from typing import Optional

from lintel import CHECKED_NODE_TYPES, Configuration, Docstring, DocstringError


class D300(DocstringError):
    description = 'Use """triple double quotes""" (found {}-quotes).'
    explanation = '''For consistency, always use """triple double quotes""" around
                     docstrings. Use r"""raw triple double quotes""" if you use any
                     backslashes in your docstrings.

                     An exception to this is made if the docstring contains
                     """-quotes in its body.
                     '''

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D300"]:
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

        error = cls(node)
        error.parameters = [illegal_quotes]

        return error


class D301(DocstringError):
    description = 'Use r""" if any backslashes are present in a docstring.'
    explanation = r'''Use r"""raw triple double quotes""" if you use any backslashes
                      (\) in your docstrings.

                      Exceptions are backslashes for line-continuation and unicode escape
                      sequences \N... and \u... These are considered intended unescaped
                      content in docstrings.
                      '''

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D301"]:
        # Just check that docstring is raw. D300 ensures the correct quotes.
        if not re.compile(r'\\[^\nuN]').search(docstring.content):
            # No backslash in docstring
            return None

        if docstring.raw.strip().startswith(('r', 'ur')):
            return None

        return cls(node)

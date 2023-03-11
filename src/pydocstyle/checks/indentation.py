"""Contains a check for proper docstring indentation."""

from typing import Generator, Union

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import CHECKED_NODE_TYPE, NODES_TO_CHECK
from pydocstyle.violations import D206, D207, D208


@check(NODES_TO_CHECK)
def check_indentation(
    _: CHECKED_NODE_TYPE, docstring: Docstring, __: Configuration
) -> Generator[Union[D206, D207, D208], None, None]:
    """D206, D207, D208: The entire docstring should be indented same as code.

    The entire docstring is indented the same as the quotes at its
    first line without using tabs.
    """
    if not docstring:
        return None

    if len(docstring.line_indents) == 0:
        return None

    if "\t" in docstring.indent or any(
        "\t" in line_indent for line_indent in docstring.line_indents
    ):
        yield D206()

    if (
        len(docstring.line_indents) > 1
        and min(docstring.line_indents[:-1]) > docstring.indent
    ) or docstring.line_indents[-1] > docstring.indent:
        yield D208()

    if min(docstring.line_indents) < docstring.indent:
        yield D207()

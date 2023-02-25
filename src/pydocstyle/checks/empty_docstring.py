import ast
from typing import Optional

from astroid import NodeNG

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import has_content
from pydocstyle.violations import D419


@check(NodeNG, terminal=True, only_if_docstring_not_empty=False)
def check_empty_docstring(
    _: NodeNG, docstring: Optional[Docstring], __: Configuration
) -> Optional[D419]:
    """D419: Docstring is empty."""
    if has_content(docstring.doc):
        return None

    return D419()

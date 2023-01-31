from typing import Optional

from pydocstyle.checks import check
from pydocstyle.parser import Class
from pydocstyle.violations import D101


@check(Class, terminal=True)
def check_missing_class_docstring(
    class_: Class, docstring: str
) -> Optional[D101]:
    """D101: Public classes should have docstrings."""
    if not class_.is_public:
        return None

    if docstring:
        return None

    return D101()

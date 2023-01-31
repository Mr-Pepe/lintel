from typing import Optional, Union

from pydocstyle.checks import check
from pydocstyle.parser import Class, NestedClass
from pydocstyle.violations import D101, D106


@check((Class, NestedClass), terminal=True)
def check_missing_class_docstring(
    class_: Class, docstring: str
) -> Optional[Union[D101, D106]]:
    """D101, D106: Public (nested) classes should have docstrings."""
    if not class_.is_public:
        return None

    if docstring:
        return None

    return D106() if isinstance(class_, NestedClass) else D101()

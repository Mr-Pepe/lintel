import pytest
from astroid import Module

from pydocstyle.docstring import Docstring, get_docstring_from_doc_node


def test_raises_error_if_node_has_no_doc_node() -> None:
    with pytest.raises(
        ValueError, match="Node 'abc' does not have a doc node."
    ):
        Docstring(Module(name="abc"))

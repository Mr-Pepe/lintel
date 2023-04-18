"""Make sure that a function signature is not repeated in the docstring."""

from typing import Optional

import astroid
from astroid import FunctionDef

from pydocstyle import Configuration, Docstring, DocstringError


class D402(DocstringError):
    description = 'First line should not be function\'s or method\'s "signature".'
    explanation = """The one-line docstring should NOT be a "signature" reiterating the
                     function/method parameters (which can be obtained by introspection).
                     """
    applicable_nodes = astroid.FunctionDef

    @classmethod
    def check_implementation(
        cls, function_: astroid.FunctionDef, docstring: Docstring, config: Configuration
    ) -> None:
        first_line = docstring.content.strip().split('\n')[0]

        if f"{function_.name}(" in first_line.replace(' ', ''):
            raise cls(function_)

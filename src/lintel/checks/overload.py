"""Make sure that `@overload` functions are not documented."""

from typing import Optional

import astroid

from lintel import Configuration, Docstring, DocstringError, is_overloaded


class D418(DocstringError):
    description = "Functions/methods decorated with @overload shouldn\'t contain a docstring."
    explanation = """Functions that are decorated with @overload are definitions,
                     and are for the benefit of the type checker only."""
    applicable_nodes = astroid.FunctionDef
    applicable_if_doc_string_is_empty = True

    @classmethod
    def check_implementation(
        cls, function_: astroid.FunctionDef, docstring: Optional[Docstring], config: Configuration
    ) -> Optional["D418"]:
        if is_overloaded(function_):
            return cls(function_)

        return None

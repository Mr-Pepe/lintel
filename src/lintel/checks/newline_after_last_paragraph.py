"""Contains a check whether closing quotes are on their own line."""

from typing import Optional

from lintel import CHECKED_NODE_TYPES, Configuration, Docstring, DocstringError, has_content


class D209(DocstringError):
    description = "Multi-line docstring closing quotes should be on a separate line."
    explanation = """Unless the entire docstring fits on a line, place the closing quotes 
                     on a line by themselves."""

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> Optional["D209"]:
        if len(docstring.lines) > 1 and docstring.raw.splitlines()[-1].strip() not in (
            '"""',
            "'''",
        ):
            return cls(node)

        return None

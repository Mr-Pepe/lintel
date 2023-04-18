"""Contains a check for proper docstring indentation."""


from pydocstyle import CHECKED_NODE_TYPES, Configuration, Docstring, DocstringError


class D206(DocstringError):
    description = "Docstring should be indented with spaces, not tabs."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> None:
        if len(docstring.line_indents) == 0:
            return None

        if "\t" in docstring.indent or any(
            "\t" in line_indent for line_indent in docstring.line_indents
        ):
            raise cls(node)


class D207(DocstringError):
    description = "Docstring is under-indented."
    explanation = (
        "The entire docstring should be indented the same as the quotes at its first line."
    )

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> None:
        if len(docstring.line_indents) == 0:
            return None

        if min(docstring.line_indents) < docstring.indent:
            raise cls(node)


class D208(DocstringError):
    description = "Docstring is over-indented."
    explanation = (
        "The entire docstring should be indented the same as the quotes at its first line."
    )

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> None:
        if len(docstring.line_indents) == 0:
            return None

        if (
            len(docstring.line_indents) > 1 and min(docstring.line_indents[:-1]) > docstring.indent
        ) or docstring.line_indents[-1] > docstring.indent:
            raise cls(node)

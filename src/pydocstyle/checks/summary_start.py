"""Contains checks regarding the summary line start of a docstring."""


from pydocstyle import (
    CHECKED_NODE_TYPES,
    Configuration,
    Docstring,
    DocstringError,
    has_content,
    is_blank,
)


class D212(DocstringError):
    description = "Multi-line docstring summary should start at the first line."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> None:
        lines = docstring.content.split('\n')

        if len(lines) > 1 and is_blank(lines[0]):
            raise cls(node)


class D213(DocstringError):
    description = "Multi-line docstring summary should start at the second line."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> None:
        lines = docstring.content.split('\n')

        if len(lines) > 1 and has_content(lines[0]):
            raise cls(node)

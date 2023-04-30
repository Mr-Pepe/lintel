"""Contains checks regarding the summary line start of a docstring."""


from pydocstyle import CHECKED_NODE_TYPES, Configuration, Docstring, DocstringError

EMPTY_FIRST_LINES = ('"""', "'''", "r'''", 'r"""', "R'''", 'R"""')


class D212(DocstringError):
    description = "Multi-line docstring summary should start at the first line."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> None:
        if len(docstring.lines) > 1 and docstring.raw.splitlines()[0].strip() in EMPTY_FIRST_LINES:
            return cls(node)


class D213(DocstringError):
    description = "Multi-line docstring summary should start at the second line."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> None:
        if (
            len(docstring.lines) > 1
            and docstring.raw.splitlines()[0].strip() not in EMPTY_FIRST_LINES
        ):
            return cls(node)

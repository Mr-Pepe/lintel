from typing import List, Optional, Tuple

import astroid

from lintel import (
    CHECKED_NODE_TYPES,
    Configuration,
    Docstring,
    DocstringError,
    has_content,
    is_blank,
    leading_space,
)


class D214(DocstringError):
    description = "Section {!r} is over-indented."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            if leading_space(section.line) > docstring.indent:
                error = cls(node)
                error.parameters = [section.name.title()]

                errors.append(error)

        return errors


class D215(DocstringError):
    description = "Section underline is over-indented in section {!r}."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            if section.underline and leading_space(section.underline.line) > docstring.indent:
                error = cls(node)
                error.parameters = [section.name.title()]

                errors.append(error)

        return errors


class D405(DocstringError):
    description = "Section name should be properly capitalized ({!r}, not {!r})."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            if section.name != section.name.title():
                error = cls(node)
                error.parameters = [section.name.title(), section.name]

                errors.append(error)

        return errors


class D406(DocstringError):
    description = "Section name should end with a newline ({!r}, not {!r})."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            suffix = section.line.strip().lstrip(section.name)

            if suffix:
                error = cls(node)
                error.parameters = [section.name.title(), section.line.strip()]

                errors.append(error)

        return errors


class D407(DocstringError):
    description = "Missing dashed underline after section {!r}."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            if not section.underline:
                error = cls(node)
                error.parameters = [section.name.title()]

                errors.append(error)

        return errors


class D408(DocstringError):
    description = "Section underline should be in the line following the section's name {!r}."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            if section.underline and set(section.following_lines[0].strip()) != {"-"}:
                error = cls(node)
                error.parameters = [section.name.title()]

                errors.append(error)

        return errors


class D409(DocstringError):
    description = "Section underline should match the length of its name {!r}."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            if section.underline and len(section.underline.line.strip()) != len(section.name):
                error = cls(node)
                error.parameters = [section.name.title(), section.name]

                errors.append(error)

        return errors


class D410(DocstringError):
    description = "Missing blank line after section {!r}."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            no_content = not section.content_lines or has_content(section.content_lines[-1])

            if not section.is_last_section and no_content:
                error = cls(node)
                error.parameters = [section.name.title()]

                errors.append(error)

        return errors


class D411(DocstringError):
    description = "Missing blank line before section {!r}."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            if has_content(section.previous_line):
                error = cls(node)
                error.parameters = [section.name.title()]

                errors.append(error)

        return errors


class D412(DocstringError):
    description = "No blank lines allowed between section header {!r} and its content."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            if len(section.content_lines) == 0:
                continue

            if not all(is_blank(line) for line in section.content_lines) and is_blank(
                section.content_lines[0]
            ):
                error = cls(node)
                error.parameters = [section.name.title()]

                errors.append(error)

        return errors


class D413(DocstringError):
    description = "Missing blank line after last section {!r}."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            if section.is_last_section and (
                has_content(section.following_lines[-1]) or not section.following_lines
            ):
                error = cls(node)
                error.parameters = [section.name.title()]

                errors.append(error)

        return errors


class D414(DocstringError):
    description = "Section {!r} has no content."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            if not section.content_lines or all(is_blank(line) for line in section.content_lines):
                error = cls(node)
                error.parameters = [section.name.title()]

                errors.append(error)

        return errors


class D416(DocstringError):
    description = "Section name should end with a colon ({!r}, not {!r})."

    @classmethod
    def check_implementation(
        cls, node: CHECKED_NODE_TYPES, docstring: Docstring, config: Configuration
    ) -> List[DocstringError]:
        errors: List[DocstringError] = []

        for section in docstring.sections:
            suffix = section.line.strip().lstrip(section.name)

            if suffix != ":":
                error = cls(node)
                error.parameters = [f"{section.name.title()}:", section.line.strip()]

                errors.append(error)

        return errors
        ...


class D417(DocstringError):
    description = "Missing argument description{} for {}."
    applicable_nodes = astroid.FunctionDef

    @classmethod
    def check_implementation(
        cls, node: astroid.FunctionDef, docstring: Docstring, config: Configuration
    ) -> Optional["D417"]:
        missing_args = [
            arg.name for arg in node.args.args if not arg.name.startswith(("_", "unused_"))
        ]

        missing_args = [arg for arg in missing_args if arg not in docstring.parameters]

        if node.is_bound():
            for arg in ["self", "cls"]:
                try:
                    missing_args.remove(arg)
                except ValueError:
                    pass

        if missing_args:
            error = cls(node)
            error.parameters = [
                "s" if len(missing_args) > 1 else "",
                ", ".join(f"'{arg}'" for arg in missing_args),
            ]

            return error

        return None

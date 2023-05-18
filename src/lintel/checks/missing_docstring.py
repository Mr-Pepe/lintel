"""Contains check for D100."""

from typing import Optional

import astroid

from lintel import (
    CHECKED_NODE_TYPES,
    VARIADIC_MAGIC_METHODS,
    Configuration,
    Docstring,
    DocstringError,
    is_dunder,
    is_nested_class,
    is_overloaded,
    is_public,
)


class D100(DocstringError):
    description = "Missing docstring in public module."
    explanation = "Public modules should have docstrings."
    applicable_nodes = astroid.Module
    applicable_if_doc_string_is_missing = True
    terminal = True

    @classmethod
    def check_implementation(
        cls,
        module: astroid.Module,
        docstring: Docstring,
        config: Configuration,
    ) -> Optional["D100"]:
        if module.doc_node is None and is_public(module) and not module.package:
            return cls(module)

        return None


class D101(DocstringError):
    description = "Missing docstring in public class."
    explanation = "Public classes should have docstrings."
    applicable_nodes = astroid.ClassDef
    applicable_if_doc_string_is_missing = True
    terminal = True

    @classmethod
    def check_implementation(
        cls,
        class_: astroid.ClassDef,
        docstring: Docstring,
        config: Configuration,
    ) -> Optional["D101"]:
        if class_.doc_node is None and is_public(class_) and not is_nested_class(class_):
            return cls(class_)

        return None


class D102(DocstringError):
    description = "Missing docstring in public method."
    explanation = "Public methods should have docstrings."
    applicable_nodes = astroid.FunctionDef
    applicable_if_doc_string_is_missing = True
    terminal = True

    @classmethod
    def check_implementation(
        cls,
        method: astroid.FunctionDef,
        docstring: Docstring,
        config: Configuration,
    ) -> Optional["D102"]:
        if (
            method.doc_node is None
            and is_public(method)
            and not is_overloaded(method)
            and method.is_bound()
            and (not is_dunder(method) or method.name in ("__new__", "__call__"))
        ):
            return cls(method)

        return None


class D103(DocstringError):
    description = "Missing docstring in public function."
    explanation = "Public functions should have docstrings."
    applicable_nodes = astroid.FunctionDef
    applicable_if_doc_string_is_missing = True
    terminal = True

    @classmethod
    def check_implementation(
        cls,
        function_: astroid.FunctionDef,
        docstring: Docstring,
        config: Configuration,
    ) -> Optional["D103"]:
        if (
            function_.doc_node is None
            and is_public(function_)
            and not is_overloaded(function_)
            and not isinstance(function_.parent, astroid.FunctionDef)
            and not function_.is_bound()
        ):
            return cls(function_)

        return None


class D104(DocstringError):
    description = "Missing docstring in public package."
    explanation = "Public packages should have docstrings."
    applicable_nodes = astroid.Module
    applicable_if_doc_string_is_missing = True
    terminal = True

    @classmethod
    def check_implementation(
        cls,
        module: CHECKED_NODE_TYPES,
        docstring: Docstring,
        config: Configuration,
    ) -> Optional["D104"]:
        if module.doc_node is None and is_public(module) and module.package:
            return cls(module)

        return None


class D105(DocstringError):
    description = "Missing docstring in magic method."
    explanation = "Magic methods should have docstrings."
    applicable_nodes = astroid.FunctionDef
    applicable_if_doc_string_is_missing = True
    terminal = True

    @classmethod
    def check_implementation(
        cls,
        method: astroid.FunctionDef,
        docstring: Docstring,
        config: Configuration,
    ) -> Optional["D105"]:
        if (
            method.doc_node is None
            and is_public(method)
            and not is_overloaded(method)
            and method.is_bound()
            and is_dunder(method)
            and not method.name in VARIADIC_MAGIC_METHODS
        ):
            return cls(method)

        return None


class D106(DocstringError):
    description = "Missing docstring in public nested class."
    explanation = "Public nested classes should have docstrings."
    applicable_nodes = astroid.ClassDef
    applicable_if_doc_string_is_missing = True
    terminal = True

    @classmethod
    def check_implementation(
        cls,
        class_: CHECKED_NODE_TYPES,
        docstring: Docstring,
        config: Configuration,
    ) -> Optional["D106"]:
        if class_.doc_node is None and is_public(class_) and is_nested_class(class_):
            return cls(class_)

        return None


class D107(DocstringError):
    description = "Missing docstring in __init__ method."
    explanation = "__init__ methods should have docstrings."
    applicable_nodes = astroid.FunctionDef
    applicable_if_doc_string_is_missing = True
    terminal = True

    @classmethod
    def check_implementation(
        cls,
        method: astroid.FunctionDef,
        docstring: Docstring,
        config: Configuration,
    ) -> Optional["D107"]:
        if (
            method.doc_node is None
            and is_public(method)
            and not is_overloaded(method)
            and method.is_bound()
            and method.name == "__init__"
        ):
            return cls(method)

        return None

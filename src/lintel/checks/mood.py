"""Contains a check for the mood of a docstring."""


from typing import Optional

import astroid
from astroid import FunctionDef

from lintel import (
    IMPERATIVE_BLACKLIST,
    IMPERATIVE_VERBS,
    Configuration,
    Docstring,
    DocstringError,
    common_prefix_length,
    get_decorator_names,
    stem,
    strip_non_alphanumeric,
)


class D401(DocstringError):
    description = "First line should be in imperative mood{}."
    explanation = """A docstring should describe the function or method's effect as a command:
                     ("Do this", "Return that"), not as a description;
                     e.g. don't write "Returns the pathname ..."."""
    applicable_nodes = astroid.FunctionDef

    @classmethod
    def check_implementation(
        cls, function_: astroid.FunctionDef, docstring: Docstring, config: Configuration
    ) -> Optional["D401"]:
        if _is_test(function_) or _is_property(function_, config):
            return None

        stripped = docstring.content.strip()

        if not stripped:
            return None

        first_word = strip_non_alphanumeric(stripped.split()[0])
        check_word = first_word.lower()

        if check_word in IMPERATIVE_BLACKLIST:
            error = cls(function_)
            error.parameters = [f" (found '{first_word}')"]

            return error

        correct_forms = IMPERATIVE_VERBS.get(stem(check_word))

        if not correct_forms or check_word in correct_forms:
            return None

        best = max(
            correct_forms,
            key=lambda f: common_prefix_length(check_word, f),
        )

        error = cls(function_)
        error.parameters = [f" (perhaps '{best.capitalize()}', not '{first_word}')"]

        return error


def _is_test(function_: FunctionDef) -> bool:
    return isinstance(function_.name, str) and (
        function_.name.startswith('test') or function_.name == 'runTest'
    )


def _is_property(function_: FunctionDef, config: Configuration) -> bool:
    return any(
        decorator in config.property_decorators for decorator in get_decorator_names(function_)
    )

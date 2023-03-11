"""Contains a check for the mood of a docstring."""

from typing import Optional, Union

from astroid import FunctionDef

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import (
    common_prefix_length,
    get_decorator_names,
    strip_non_alphanumeric,
)
from pydocstyle.violations import D401, D401b
from pydocstyle.wordlists import IMPERATIVE_BLACKLIST, IMPERATIVE_VERBS, stem


@check(FunctionDef)
def check_imperative_mood(
    function_: FunctionDef, docstring: Docstring, config: Configuration
) -> Optional[Union[D401, D401b]]:
    """D401: First line should be in imperative mood: 'Do', not 'Does'.

    [Docstring] prescribes the function or method's effect as a command:
    ("Do this", "Return that"), not as a description; e.g. don't write
    "Returns the pathname ...".
    """
    if _is_test(function_) or _is_property(function_, config):
        return None

    stripped = docstring.content.strip()

    if not stripped:
        return None

    first_word = strip_non_alphanumeric(stripped.split()[0])
    check_word = first_word.lower()
    correct_forms = IMPERATIVE_VERBS.get(stem(check_word))

    if check_word in IMPERATIVE_BLACKLIST:
        return D401b(first_word)

    if not correct_forms or check_word in correct_forms:
        return None

    best = max(
        correct_forms,
        key=lambda f: common_prefix_length(check_word, f),
    )
    return D401(best.capitalize(), first_word)


def _is_test(function_: FunctionDef) -> bool:
    return isinstance(function_.name, str) and (
        function_.name.startswith('test') or function_.name == 'runTest'
    )


def _is_property(function_: FunctionDef, config: Configuration) -> bool:
    return any(
        decorator in config.property_decorators
        for decorator in get_decorator_names(function_)
    )

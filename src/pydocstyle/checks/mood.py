import ast
from typing import Optional, Union

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.parser import Function
from pydocstyle.utils import common_prefix_length, strip_non_alphanumeric
from pydocstyle.violations import D401, D401b
from pydocstyle.wordlists import IMPERATIVE_BLACKLIST, IMPERATIVE_VERBS, stem


@check(Function)
def check_imperative_mood(
    function: Function, docstring: str, config: Configuration
) -> Optional[Union[D401, D401b]]:
    """D401: First line should be in imperative mood: 'Do', not 'Does'.

    [Docstring] prescribes the function or method's effect as a command:
    ("Do this", "Return that"), not as a description; e.g. don't write
    "Returns the pathname ...".
    """
    if not docstring:
        return None

    if function.is_test or function.is_property(config.property_decorators):
        return None

    stripped = ast.literal_eval(docstring).strip()

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

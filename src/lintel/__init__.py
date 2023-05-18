from enum import Enum
from typing import Union

import astroid

from ._version import __version__


class Convention(Enum):
    """The supported docstring conventions."""

    NONE = "none"
    ALL = "all"
    DEFAULT = "default"
    NUMPY = "numpy"
    GOOGLE = "google"


CHECKED_NODE_TYPES = Union[
    astroid.ClassDef,
    astroid.FunctionDef,
    astroid.Module,
]
NODES_TO_CHECK = (
    astroid.ClassDef,
    astroid.FunctionDef,
    astroid.Module,
)

# TODO: Remove stuff that is only used in one module


CONVENTION_ERRORS = {
    Convention.DEFAULT: {
        "D100",
        "D101",
        "D102",
        "D103",
        "D104",
        "D105",
        "D106",
        "D107",
        "D200",
        "D201",
        "D202",
        "D204",
        "D205",
        "D206",
        "D207",
        "D208",
        "D209",
        "D210",
        "D211",
        "D300",
        "D301",
        "D400",
        "D401",
        "D402",
        "D403",
        "D412",
        "D414",
        "D418",
        "D419",
    },
    Convention.NUMPY: {
        "D100",
        "D101",
        "D102",
        "D103",
        "D104",
        "D105",
        "D106",
        "D200",
        "D201",
        "D202",
        "D204",
        "D205",
        "D206",
        "D207",
        "D208",
        "D209",
        "D210",
        "D211",
        "D214",
        "D215",
        "D300",
        "D301",
        "D400",
        "D401",
        "D403",
        "D404",
        "D405",
        "D406",
        "D407",
        "D408",
        "D409",
        "D410",
        "D411",
        "D412",
        "D414",
        "D417",
        "D418",
        "D419",
    },
    Convention.GOOGLE: {
        "D100",
        "D101",
        "D102",
        "D103",
        "D104",
        "D105",
        "D106",
        "D107",
        "D200",
        "D201",
        "D202",
        "D205",
        "D206",
        "D207",
        "D208",
        "D209",
        "D210",
        "D211",
        "D212",
        "D214",
        "D300",
        "D301",
        "D402",
        "D403",
        "D405",
        "D410",
        "D411",
        "D412",
        "D414",
        "D415",
        "D416",
        "D417",
        "D418",
        "D419",
    },
}

from ._config import (
    DEFAULT_MATCH,
    DEFAULT_MATCH_DIR,
    DEFAULT_PROPERTY_DECORATORS,
    Configuration,
    IllegalConfiguration,
    load_config,
)
from ._file_discovery import discover_files
from ._utils import *

# isort: split


from ._docstring import Docstring, Section, get_docstring_from_doc_node
from ._docstring_error import DocstringError
from ._get_checks import get_checks
from ._wordlists import IMPERATIVE_BLACKLIST, IMPERATIVE_VERBS, stem

# isort: split

from ._get_error_codes import (
    _get_definition_line,
    get_all_error_codes,
    get_error_codes,
    get_error_codes_to_skip,
    get_line_noqa,
)

# isort: split

from ._check_source import check_source

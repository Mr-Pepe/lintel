from enum import Enum

from ._node_types import CHECKED_NODE_TYPES, NODES_TO_CHECK


class Convention(Enum):
    PEP257 = "pep257"
    NUMPY = "numpy"
    GOOGLE = "google"


from ._config import Configuration, IllegalConfiguration
from ._utils import *
from ._version import __version__
from ._wordlists import IMPERATIVE_BLACKLIST, IMPERATIVE_VERBS, stem

# isort: split


from ._docstring import Docstring, get_docstring_from_doc_node
from ._docstring_error import DocstringError
from ._get_checks import get_checks, get_error_codes

# isort: split

from ._check_source import check_source

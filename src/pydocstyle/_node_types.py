from typing import Union

import astroid

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

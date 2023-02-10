from typing import Callable, Tuple, Union

from pydocstyle.parser import Definition


def check(
    node_type: Union[Definition, Tuple[Definition, ...]],
    terminal: bool = False,
) -> Callable:
    """Decorate check with the node type it's applicable for.

    Also set whether a failure should stop further check executions.
    """

    def decorator(check: Callable) -> Callable:
        check._node_type = node_type  # type: ignore
        check._terminal = terminal  # type: ignore
        return check

    return decorator

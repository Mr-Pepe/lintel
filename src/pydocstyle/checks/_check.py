from typing import Any, Callable, Optional, Tuple, Union

from pydocstyle.parser import Definition
from pydocstyle.violations import Error


class Check:
    def __init__(
        self,
        node_type: Union[Definition, Tuple[Definition, ...]],
        terminal: bool,
        check_function: Callable[..., Optional[Error]],
    ) -> None:
        self._node_type = node_type
        self._terminal = terminal
        self.check_function = check_function

    def __call__(self, *args: Any, **kwargs: Any) -> Error:
        check_result = self.check_function(*args, *kwargs)
        return check_result

    @property
    def explanation(self) -> Optional[str]:
        return self.check_function.__doc__


def check(
    node_type: Union[Definition, Tuple[Definition, ...]],
    terminal: bool = False,
) -> Callable[[Callable[..., Optional[Error]]], Check]:
    """Decorate check with the node type it's applicable for.

    Also set whether a failure should stop further check executions.
    """

    def decorator(check_function: Callable[..., Optional[Error]]) -> Check:
        return Check(
            node_type=node_type,
            terminal=terminal,
            check_function=check_function,
        )

    return decorator

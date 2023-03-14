from typing import Any, Callable, Optional, Tuple, Union

from astroid import NodeNG

from pydocstyle.violations import Error


class Check:
    """Represents a specific docstring check."""

    def __init__(
        self,
        node_type: Union[NodeNG, Tuple[NodeNG, ...]],
        terminal: bool,
        only_if_docstring_exists: bool,
        only_if_docstring_not_empty: bool,
        check_function: Callable[..., Optional[Error]],
    ) -> None:
        """Initialize the check."""
        self.node_type = node_type
        self.terminal = terminal
        self.only_if_docstring_exists = only_if_docstring_exists
        self.only_if_docstring_not_empty = only_if_docstring_not_empty
        self.check_function = check_function

    def __call__(self, *args: Any, **kwargs: Any) -> Error:
        """Execute the check."""
        check_result = self.check_function(*args, *kwargs)
        return check_result

    @property
    def explanation(self) -> Optional[str]:
        return self.check_function.__doc__


def check(
    node_type: Union[NodeNG, Tuple[NodeNG, ...]],
    terminal: bool = False,
    only_if_docstring_exists: bool = True,
    only_if_docstring_not_empty: bool = True,
) -> Callable[[Callable[..., Optional[Error]]], Check]:
    """Add a pydoclint check.

    Args:
        node_type: The astroid node types the check is applicable for.
        terminal: Whether a failure should stop further check executions.
            Defaults to False.
        only_if_docstring_exists: Whether the check should only be
            executed if a docstring exists. Defaults to True.
        only_if_docstring_not_empty: Whether the check should only be
            executed if the docstring is not empty. Defaults to True.
    """

    def decorator(check_function: Callable[..., Optional[Error]]) -> Check:
        return Check(
            node_type=node_type,
            terminal=terminal,
            only_if_docstring_exists=only_if_docstring_exists,
            only_if_docstring_not_empty=only_if_docstring_not_empty,
            check_function=check_function,
        )

    return decorator

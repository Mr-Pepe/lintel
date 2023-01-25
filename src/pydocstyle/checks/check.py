from pydocstyle.parser import Definition


def check(node_type: Definition, terminal: bool = False):
    """Decorate check with the node type it's applicable for.

    Also set whether a failure should stop further check executions.
    """

    def decorator(check):
        check._node_type = node_type
        check._terminal = terminal
        return check

    return decorator

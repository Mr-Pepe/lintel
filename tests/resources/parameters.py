"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


class A:

    """My class.

    Args:
        param1: The first parameter.
    """

    def __init__(self, param1):
        """Does something.

        Args:
            param1: The first parameter.
        """

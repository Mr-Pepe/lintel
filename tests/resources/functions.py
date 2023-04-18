# fmt: off

"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


@expect("D201: No blank lines allowed before function/method docstring (found 1).")
def func_with_space_before():

    """Test a function with space before docstring."""
    pass


@expect("D202: No blank lines allowed after function/method docstring (found 1).")
def func_with_space_after():
    """Test a function with space after docstring."""

    pass


def func_with_inner_func_after():
    """Test a function with inner function after docstring."""

    def inner_after():
        pass

    pass


def func_with_inner_async_func_after():
    """Test a function with inner async function after docstring."""

    async def inner_async():
        pass

    pass


def fake_decorator(decorated):
    """Fake decorator used to test decorated inner func."""
    return decorated


def func_with_inner_decorated_func_after():
    """Test a function with inner decorated function after docstring."""

    @fake_decorator
    def inner_decorated():
        pass

    pass


def func_with_inner_decorated_async_func_after():
    """Test a function with inner decorated async function after docstring."""

    @fake_decorator
    async def inner_async_decoreated():
        pass

    pass


def func_with_inner_class_after():
    """Test a function with inner class after docstring."""

    class inner_class:
        pass

    pass


def func_with_weird_backslash():
    """Test a function with a weird backslash.\
"""

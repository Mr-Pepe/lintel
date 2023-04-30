# fmt: off
"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


_D400 = "D400: First line should end with a period (not '!')."

@expect("D405: Section name should be properly capitalized "
        "('Returns', not 'returns').")
def not_capitalized():
    """Toggle the gizmo.

    returns
    -------
    A value of some sort.

    """



@expect("D406: Section name should end with a newline "
        "('Returns', not 'Returns:').")
def superfluous_suffix():
    """Toggle the gizmo.

    Returns:
    -------
    A value of some sort.

    """



@expect("D407: Missing dashed underline after section 'Returns'.")
def no_underline():
    """Toggle the gizmo.

    Returns
    A value of some sort.

    """


@expect("D407: Missing dashed underline after section 'Returns'.")
@expect("D414: Section 'Returns' has no content.")
def no_underline_and_no_description():
    """Toggle the gizmo.

    Returns

    """


@expect("D410: Missing blank line after section 'Returns'.")
@expect("D414: Section 'Returns' has no content.")
@expect("D411: Missing blank line before section 'Yields'.")
@expect("D414: Section 'Yields' has no content.")
def consecutive_sections():
    """Toggle the gizmo.

    Returns
    -------
    Yields
    ------

    Raises
    ------
    Questions.

    """


@expect("D408: Section underline should be in the line following the "
        "section's name 'Returns'.")
def blank_line_before_underline():
    """Toggle the gizmo.

    Returns

    -------
    A value of some sort.

    """



@expect("D409: Section underline should match the length of its name 'Returns'.")
def bad_underline_length():
    """Toggle the gizmo.

    Returns
    --
    A value of some sort.

    """


@expect("D411: Missing blank line before section 'Returns'.")
def no_blank_line_before_section():
    """Toggle the gizmo.

    The function's description.
    Returns
    -------
    A value of some sort.

    """


@expect("D214: Section 'Returns' is over-indented.")
def section_overindented():
    """Toggle the gizmo.

        Returns
    -------
    A value of some sort.

    """


@expect("D215: Section underline is over-indented in section 'Returns'.")
def section_underline_overindented():
    """Toggle the gizmo.

    Returns
        -------
    A value of some sort.

    """


@expect("D215: Section underline is over-indented in section 'Returns'.")
@expect("D414: Section 'Returns' has no content.")
def section_underline_overindented_and_contentless():
    """Toggle the gizmo.

    Returns
        -------
    """


def ignore_non_actual_section():
    """Toggle the gizmo.

    This is the function's description, which will also specify what it
    returns

    """


@expect("D401: First line should be in imperative mood "
        "(perhaps 'Return', not 'Returns').")
@expect("D400: First line should end with a period (not 's').")
@expect("D205: 1 blank line required between summary line and description "
        "(found 0).")
def section_name_in_first_line():
    """Returns
    -------
    A value of some sort.

    """


@expect("D405: Section name should be properly capitalized "
        "('Short Summary', not 'Short summary').")
@expect("D412: No blank lines allowed between section header 'Short Summary' and its content.")
@expect("D409: Section underline should match the length of its name 'Returns'.")
@expect("D410: Missing blank line after section 'Returns'.")
@expect("D411: Missing blank line before section 'Raises'.")
@expect("D406: Section name should end with a newline "
        "('Raises', not 'Raises:').")
@expect("D407: Missing dashed underline after section 'Raises'.")
def multiple_sections():
    """Toggle the gizmo.

    Short summary
    -------------

    This is the function's description, which will also specify what it
    returns.

    Returns
    ------
    Many many wonderful things.
    Raises:
    My attention.

    """



def false_positive_section_prefix():
    """Toggle the gizmo.

    Parameters
    ----------
    attributes_are_fun: attributes for the function.

    """



def section_names_as_parameter_names():
    """Toggle the gizmo.

    Parameters
    ----------
    notes : list
        A list of wonderful notes.
    examples: list
        A list of horrible examples.

    """

@expect("D207: Docstring is under-indented.", func_name="bar")
@expect("D417: Missing argument description for 'y'.", func_name="bar")
def _test_nested_functions():
    x = 1

    def bar(y=2):
        """Nested function test for docstrings.

        Will this work when referencing x?

        Parameters
        ----------
            x: Test something
that is broken.

        """
        ...


@expect("D417: Missing argument description for 'y'.")
def test_missing_numpy_args(_private_arg=0, x=1, y=2):
    """Toggle the gizmo.

    Parameters
    ----------
    x : int
        The greatest integer in the history \
of the entire world.

    """


class TestNumpy:
    """Test class."""

    def test_method(self, test, another_test, z, _, x=1, y=2, _private_arg=1):
        """Test a valid args section.

        Some long string with a \
line continuation.

        Parameters
        ----------
        test, another_test
            Some parameters without type.
        z : some parameter with a very long type description that requires a \
line continuation.
            But no further description.
        x, y : int
            Some integer parameters.

        """

    @expect("D417: Missing argument descriptions for 'test', 'y', 'z'.", arg_count=5)
    def test_missing_args(self, test, x, y, z=3, t=1, _private=0):
        """Test a valid args section.

        Parameters
        ----------
        x, t : int
            Some parameters.


        """

    @classmethod
    @expect("D417: Missing argument descriptions for 'test', 'y', 'z'.", arg_count=4)
    def test_missing_args_class_method(cls, test, x, y, z=3):
        """Test a valid args section.

        Parameters
        ----------
        z
        x
            Another parameter. The parameters y, test below are
            missing descriptions. The parameter z above is also missing
            a description.
        y
        test

        """

    @staticmethod
    @expect("D417: Missing argument descriptions for 'a', 'z'.", arg_count=3)
    def test_missing_args_static_method(a, x, y, z=3, t=1):
        """Test a valid args section.

        Parameters
        ----------
        x, y
            Another parameter.
        t : int
            Yet another parameter.

        """

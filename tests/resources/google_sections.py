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

    returns:
        A value of some sort.

    """


@expect("D414: Section 'Returns' has no content.")
def no_underline_and_no_description():
    """Toggle the gizmo.

    Returns:

    """

@expect("D416: Section name should end with a colon ('Returns:', not 'Returns').")
def consecutive_sections():
    """Toggle the gizmo.

    Returns
    Yields

    Raises:
        Questions.

    """


@expect("D411: Missing blank line before section 'Returns'.")
def no_blank_line_before_section():
    """Toggle the gizmo.

    The function's description.
    Returns:
        A value of some sort.

    """


@expect("D208: Docstring is over-indented.")
@expect("D214: Section 'Returns' is over-indented.")
def section_overindented():
    """Toggle the gizmo.

        Returns:
        A value of some sort.

    """


def ignore_non_actual_section():
    """Toggle the gizmo.

    This is the function's description, which will also specify what it
    returns

    """


@expect("D415: First line should end with a period, question "
        "mark, or exclamation point (not 's').")
@expect("D205: 1 blank line required between summary line and description "
        "(found 0).")
def section_name_in_first_line():
    """Returns
    A value of some sort.

    """


@expect("D410: Missing blank line after section 'Returns'.")
@expect("D411: Missing blank line before section 'Raises'.")
@expect("D416: Section name should end with a colon ('Returns:', not 'Returns').")
def multiple_sections():
    """Toggle the gizmo.

    This is the function's description, which will also specify what it
    returns.

    Returns
        Many many wonderful things.
    Raises:
        My attention.

    """


def section_names_as_parameter_names():
    """Toggle the gizmo.

    Args:
        notes : list
            A list of wonderful notes.
        examples: list
            A list of horrible examples.

    """


@expect("D414: Section 'Returns' has no content.")
def valid_google_style_section():
    """Toggle the gizmo.

    Args:
        note: A random string.

    Returns:

    Raises:
        RandomError: A random error that occurs randomly.

    """



@expect("D416: Section name should end with a colon "
        "('Args:', not 'Args').")
def missing_colon_google_style_section():
    """Toggle the gizmo.

    Args
        note: A random string.

    """

@expect("D207: Docstring is under-indented.", func_name="bar")
@expect("D417: Missing argument description for 'y'.", func_name="bar")
def _test_nested_functions():
    x = 1

    def bar(y=2):
        """Nested function test for docstrings.

        Will this work when referencing x?

        Args:
            x: Test something
that is broken.

        """
        ...



@expect("D417: Missing argument description for 'y'.")
def test_private_args_ignored(x=1, y=2, _private=3):
    """Toggle the gizmo.

    Args:
        x (int): The greatest integer.

    """

@expect("D417: Missing argument description for 'y'.")
def test_unused_args_ignored(x=1, y=2, unused_args=3):
    """Toggle the gizmo.

    Args:
        x (int): The greatest integer.

    """

class TestGoogle:
    """Test class."""

    def test_method(self, test, another_test, _):
        """Test a valid args section.

        Args:
            test: A parameter.
            another_test: Another parameter.

        """

    def test_detailed_description(self, test, another_test, _):
        """Test a valid args section.

        Args:
            test: A parameter.
            another_test: Another parameter.

        Detailed description.

        """

    @expect("D417: Missing argument descriptions for 'test', 'y', 'z'.", arg_count=5)
    def test_missing_args(self, test, x, y, z=3, _private_arg=3):
        """Test a valid args section.

        Args:
            x: Another parameter.

        """

    @classmethod
    @expect("D417: Missing argument descriptions for 'test', 'y', 'z'.", arg_count=5)
    def test_missing_args_class_method(cls, test, x, y, _, z=3):
        """Test a valid args section.

        Args:
            x: Another parameter. The parameter below is missing description.
            y:

        """

    @staticmethod
    @expect("D417: Missing argument descriptions for 'a', 'y', 'z'.", arg_count=4)
    def test_missing_args_static_method(a, x, y, _test, z=3):
        """Test a valid args section.

        Args:
            x: Another parameter.

        """

    @staticmethod
    @expect("D417: Missing argument descriptions for 'a', 'b'.", arg_count=2)
    def test_missing_docstring(a, b):
        """Test a valid args section.

        Args:
            a:

        """

    @staticmethod
    def test_hanging_indent(skip, verbose):
        """Do stuff.

        Args:
            skip (:attr:`.Skip`):
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Etiam at tellus a tellus faucibus maximus. Curabitur tellus
                mauris, semper id vehicula ac, feugiat ut tortor.
            verbose (bool):
                If True, print out as much infromation as possible.
                If False, print out concise "one-liner" information.

        """


class TestIncorrectIndent:
    """Test class."""

    @expect("D207: Docstring is under-indented.", arg_count=3)
    @expect("D417: Missing argument description for 'y'.", arg_count=3)
    def test_incorrect_indent(self, x=1, y=2):
        """Reproducing issue #437.

Testing this incorrectly indented docstring.

        Args:
            x: Test argument.

        """

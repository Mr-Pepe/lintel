"""Contains checks for docstring sections."""

import re
from collections import namedtuple
from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Generator, List, Optional, Set, Tuple, Union

from astroid import FunctionDef

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import (
    CHECKED_NODE_TYPE,
    NODES_TO_CHECK,
    get_leading_words,
    is_blank,
    leading_space,
    pairwise,
)
from pydocstyle.violations import (
    D214,
    D215,
    D405,
    D406,
    D407,
    D408,
    D409,
    D410,
    D411,
    D412,
    D413,
    D414,
    D416,
    D417,
)


@dataclass
class SectionContext:
    """Holds information about a docstring section."""

    section_name: str
    previous_line: str
    line: str
    following_lines: List[str]
    original_index: int
    is_last_section: bool


NUMPY_SECTION_NAMES = (
    'Short Summary',
    'Extended Summary',
    'Parameters',
    'Returns',
    'Yields',
    'Other Parameters',
    'Raises',
    'See Also',
    'Notes',
    'References',
    'Examples',
    'Attributes',
    'Methods',
)

GOOGLE_SECTION_NAMES = (
    'Args',
    'Arguments',
    'Attention',
    'Attributes',
    'Caution',
    'Danger',
    'Error',
    'Example',
    'Examples',
    'Hint',
    'Important',
    'Keyword Args',
    'Keyword Arguments',
    'Methods',
    'Note',
    'Notes',
    'Return',
    'Returns',
    'Raises',
    'References',
    'See Also',
    'Tip',
    'Todo',
    'Warning',
    'Warnings',
    'Warns',
    'Yield',
    'Yields',
)

# Examples that will be matched -
# "     random: Test" where random will be captured as the param
# " random         : test" where random will be captured as the param
# "  random_t (Test) : test  " where random_t will be captured as the param
# Matches anything that fulfills all the following conditions:
GOOGLE_ARGS_REGEX = re.compile(
    # Begins with 0 or more whitespace characters
    r"^\s*"
    # Followed by 1 or more unicode chars, numbers or underscores
    # The above is captured as the first group as this is the paramater name.
    r"(\w+)"
    # Followed by 0 or more whitespace characters
    r"\s*"
    # Matches patterns contained within round brackets.
    # The `.*?`matches any sequence of characters in a non-greedy
    # way (denoted by the `*?`)
    r"(\(.*?\))?"
    # Followed by 0 or more whitespace chars
    r"\s*"
    # Followed by a colon
    r":"
    # Might have a new line and leading whitespace
    r"\n?\s*"
    # Followed by 1 or more characters - which is the docstring for the parameter
    ".+"
)


def _is_docstring_section(context):
    """Check if the suspected context is really a section header.

    Lets have a look at the following example docstring:
        '''Title.

        Some part of the docstring that specifies what the function
        returns. <----- Not a real section name. It has a suffix and the
                        previous line is not empty and does not end with
                        a punctuation sign.

        This is another line in the docstring. It describes stuff,
        but we forgot to add a blank line between it and the section name.
        Parameters  <-- A real section name. The previous line ends with
        ----------      a period, therefore it is in a new
                        grammatical context.
        param : int
        examples : list  <------- Not a section - previous line doesn't end
            A list of examples.   with punctuation.
        notes : list  <---------- Not a section - there's text after the
            A list of notes.      colon.

        Notes:  <--- Suspected as a context because there's a suffix to the
        -----        section, but it's a colon so it's probably a mistake.
        Bla.

        '''

    To make sure this is really a section we check these conditions:
        * There's no suffix to the section name or it's just a colon AND
        * The previous line is empty OR it ends with punctuation.

    If one of the conditions is true, we will consider the line as
    a section name.
    """
    section_name_suffix = (
        context.line.strip().lstrip(context.section_name.strip()).strip()
    )

    section_suffix_is_only_colon = section_name_suffix == ':'

    punctuation = [',', ';', '.', '-', '\\', '/', ']', '}', ')']
    prev_line_ends_with_punctuation = any(
        context.previous_line.strip().endswith(x) for x in punctuation
    )

    this_line_looks_like_a_section_name = (
        is_blank(section_name_suffix) or section_suffix_is_only_colon
    )

    prev_line_looks_like_end_of_paragraph = (
        prev_line_ends_with_punctuation or is_blank(context.previous_line)
    )

    return (
        this_line_looks_like_a_section_name
        and prev_line_looks_like_end_of_paragraph
    )


def _check_blanks_and_section_underline(section_name, context, indentation):
    """D4{07,08,09,12,14}, D215: Section underline checks.

    Check for correct formatting for docstring sections. Checks that:
        * The line that follows the section name contains
            dashes (D40{7,8}).
        * The amount of dashes is equal to the length of the section
            name (D409).
        * The section's content does not begin in the line that follows
            the section header (D412).
        * The section has no content (D414).
        * The indentation of the dashed line is equal to the docstring's
            indentation (D215).
    """
    blank_lines_after_header = 0

    for line in context.following_lines:
        if not is_blank(line):
            break
        blank_lines_after_header += 1
    else:
        # There are only blank lines after the header.
        yield D407(section_name)
        yield D414(section_name)
        return

    non_empty_line = context.following_lines[blank_lines_after_header]
    dash_line_found = ''.join(set(non_empty_line.strip())) == '-'

    if not dash_line_found:
        yield D407(section_name)
        if blank_lines_after_header > 0:
            yield D412(section_name)
    else:
        if blank_lines_after_header > 0:
            yield D408(section_name)

        if non_empty_line.strip() != "-" * len(section_name):
            yield D409(
                len(section_name),
                section_name,
                len(non_empty_line.strip()),
            )

        if leading_space(non_empty_line) > indentation:
            yield D215(section_name)

        line_after_dashes_index = blank_lines_after_header + 1
        # If the line index after the dashes is in range (perhaps we have
        # a header + underline followed by another section header).
        if line_after_dashes_index < len(context.following_lines):
            line_after_dashes = context.following_lines[
                line_after_dashes_index
            ]
            if is_blank(line_after_dashes):
                rest_of_lines = context.following_lines[
                    line_after_dashes_index:
                ]
                if not is_blank(''.join(rest_of_lines)):
                    yield D412(section_name)
                else:
                    yield D414(section_name)
        else:
            yield D414(section_name)


def _check_common_section(
    docstring: Docstring,
    context: SectionContext,
    valid_section_names: Tuple[str, ...],
) -> Generator[Union[D405, D214, D413, D410, D411], None, None]:
    """D4{05,10,11,13}, D214: Section name checks.

    Check for valid section names. Checks that:
        * The section name is properly capitalized (D405).
        * The section is not over-indented (D214).
        * There's a blank line after the section (D410, D413).
        * There's a blank line before the section (D411).

    Also yields all the errors from `_check_blanks_and_section_underline`.
    """
    indentation = docstring.indent
    capitalized_section = context.section_name.title()

    if (
        context.section_name not in valid_section_names
        and capitalized_section in valid_section_names
    ):
        yield D405(capitalized_section, context.section_name)

    if leading_space(context.line) > indentation:
        yield D214(capitalized_section)

    if not context.following_lines or not is_blank(
        context.following_lines[-1]
    ):
        if context.is_last_section:
            yield D413(capitalized_section)
        else:
            yield D410(capitalized_section)

    if not is_blank(context.previous_line):
        yield D411(capitalized_section)

    yield from _check_blanks_and_section_underline(
        capitalized_section, context, indentation
    )


def _check_numpy_section(
    node: CHECKED_NODE_TYPE, docstring: Docstring, context: SectionContext
) -> Generator[D406, None, None]:
    """D406: NumPy-style section name checks.

    Check for valid section names. Checks that:
        * The section name has no superfluous suffix to it (D406).

    Additionally, also yield all violations from `_check_common_section`
    which are style-agnostic section checks.
    """
    capitalized_section = context.section_name.title()

    yield from _check_common_section(docstring, context, NUMPY_SECTION_NAMES)

    suffix = context.line.strip().lstrip(context.section_name)

    if suffix:
        yield D406(capitalized_section, context.line.strip())

    if capitalized_section == "Parameters":
        yield from _check_parameters_section(node, context)


def _check_parameters_section(
    node: CHECKED_NODE_TYPE, context: SectionContext
) -> Generator:
    """D417: `Parameters` section check for numpy style.

    Check for a valid `Parameters` section. Checks that:
        * The section documents all function arguments (D417)
            except `self` or `cls` if it is a method.

    """
    docstring_args = set()
    section_level_indent = leading_space(context.line)
    # Join line continuations, then resplit by line.
    content = (
        '\n'.join(context.following_lines).replace('\\\n', '').split('\n')
    )
    for current_line, next_line in zip(content, content[1:]):
        # All parameter definitions in the Numpy parameters
        # section must be at the same indent level as the section
        # name.
        # Also, we ensure that the following line is indented,
        # and has some string, to ensure that the parameter actually
        # has a description.
        # This means, this is a parameter doc with some description
        if (
            (leading_space(current_line) == section_level_indent)
            and (
                len(leading_space(next_line))
                > len(leading_space(current_line))
            )
            and next_line.strip()
        ):
            # In case the parameter has type definitions, it
            # will have a colon
            if ":" in current_line:
                parameters, parameter_type = current_line.split(":", 1)
            # Else, we simply have the list of parameters defined
            # on the current line.
            else:
                parameters = current_line.strip()
            # Numpy allows grouping of multiple parameters of same
            # type in the same line. They are comma separated.
            parameter_list = parameters.split(",")
            for parameter in parameter_list:
                docstring_args.add(parameter.strip())
    yield from _check_missing_args(node, docstring_args)


def _check_args_section(
    node: CHECKED_NODE_TYPE, context: SectionContext
) -> Generator:
    """D417: `Args` section checks.

    Check for a valid `Args` or `Argument` section. Checks that:
        * The section documents all function arguments (D417)
            except `self` or `cls` if it is a method.

    Documentation for each arg should start at the same indentation
    level. For example, in this case x and y are distinguishable::

        Args:
            x: Lorem ipsum dolor sit amet
            y: Ut enim ad minim veniam

    In the case below, we only recognize x as a documented parameter
    because the rest of the content is indented as if it belongs
    to the description for x::

        Args:
            x: Lorem ipsum dolor sit amet
                y: Ut enim ad minim veniam
    """
    docstring_args = set()

    # normalize leading whitespace
    if context.following_lines:
        # any lines with shorter indent than the first one should be disregarded
        first_line = context.following_lines[0]
        leading_whitespaces = first_line[: -len(first_line.lstrip())]

    args_content = dedent(
        "\n".join(
            [
                line
                for line in context.following_lines
                if line.startswith(leading_whitespaces) or line == ""
            ]
        )
    ).strip()

    args_sections = []
    for line in args_content.splitlines(keepends=True):
        if not line[:1].isspace():
            # This line is the start of documentation for the next
            # parameter because it doesn't start with any whitespace.
            args_sections.append(line)
        else:
            # This is a continuation of documentation for the last
            # parameter because it does start with whitespace.
            args_sections[-1] += line

    for section in args_sections:
        match = GOOGLE_ARGS_REGEX.match(section)
        if match:
            docstring_args.add(match.group(1))
    yield from _check_missing_args(node, docstring_args)


def _check_missing_args(
    node: CHECKED_NODE_TYPE, docstring_args: Set[str]
) -> Generator[D417, None, None]:
    """D417: Yield error for missing arguments in docstring.

    Given a list of arguments found in the docstring and the
    callable definition, it checks if all the arguments of the
    callable are present in the docstring, else it yields a
    D417 with a list of missing arguments.

    """
    if isinstance(node, FunctionDef):
        required_args = set(
            arg.name
            for arg in node.args.args
            if arg.name not in ("self", "cls") and not arg.name.startswith("_")
        )

        missing_args = required_args - docstring_args

        if missing_args:
            yield D417(", ".join(sorted(missing_args)), node.name)


def _check_google_section(node, docstring, context):
    """D416: Google-style section name checks.

    Check for valid section names. Checks that:
        * The section does not contain any blank line between its name
            and content (D412).
        * The section is not empty (D414).
        * The section name has colon as a suffix (D416).

    Additionally, also yield all violations from `_check_common_section`
    which are style-agnostic section checks.
    """
    capitalized_section = context.section_name.title()
    yield from _check_common_section(docstring, context, GOOGLE_SECTION_NAMES)
    suffix = context.line.strip().lstrip(context.section_name)
    if suffix != ":":
        yield D416(capitalized_section + ":", context.line.strip())

    if capitalized_section in ("Args", "Arguments"):
        yield from _check_args_section(node, context)


def _get_section_contexts(
    lines: List[str], valid_section_names: Tuple[str, ...]
) -> Generator[SectionContext, None, None]:
    """Generate `SectionContext` objects for valid sections.

    Given a list of `valid_section_names`, generate an
    `Iterable[SectionContext]` which provides:
        * Section Name
        * String value of the previous line
        * The section line
        * Following lines till the next section
        * Line index of the beginning of the section in the docstring
        * Boolean indicating whether the section is the last section.
    for each valid section.

    """
    lower_section_names = [s.lower() for s in valid_section_names]

    def _suspected_as_section(_line):
        result = get_leading_words(_line.lower())
        return result in lower_section_names

    # Finding our suspects.
    suspected_section_indices = [
        i for i, line in enumerate(lines) if _suspected_as_section(line)
    ]

    # First - create a list of possible contexts. Note that the
    # `following_lines` member is until the end of the docstring.
    contexts = (
        SectionContext(
            get_leading_words(lines[i].strip()),
            lines[i - 1],
            lines[i],
            lines[i + 1 :],
            i,
            False,
        )
        for i in suspected_section_indices
    )

    # Now that we have manageable objects - rule out false positives.
    contexts = (c for c in contexts if _is_docstring_section(c))

    # Now we shall trim the `following lines` field to only reach the
    # next section name.
    for a, b in pairwise(contexts, None):
        end = -1 if b is None else b.original_index
        yield SectionContext(
            a.section_name,
            a.previous_line,
            a.line,
            lines[a.original_index + 1 : end],
            a.original_index,
            b is None,
        )


def _check_numpy_sections(
    node: CHECKED_NODE_TYPE, docstring: Docstring
) -> Generator[Any, None, bool]:
    """NumPy-style docstring sections checks.

    Check the general format of a sectioned docstring:
        '''This is my one-liner.

        Short Summary
        -------------
        This is my summary.

        Returns
        -------
        None.

        '''

    Section names appear in `NUMPY_SECTION_NAMES`.
    Yields all violation from `_check_numpy_section` for each valid
    Numpy-style section.
    """
    found_any_numpy_section = False
    for context in _get_section_contexts(
        docstring.content.split("\n"), NUMPY_SECTION_NAMES
    ):
        found_any_numpy_section = True
        yield from _check_numpy_section(node, docstring, context)

    return found_any_numpy_section


def _check_google_sections(
    node: CHECKED_NODE_TYPE, docstring: Docstring
) -> Generator:
    """Google-style docstring section checks.

    Check the general format of a sectioned docstring:
        '''This is my one-liner.

        Note:
            This is my summary.

        Returns:
            None.

        '''

    Section names appear in `GOOGLE_SECTION_NAMES`.
    Yields all violation from `_check_google_section` for each valid
    Google-style section.
    """
    for context in _get_section_contexts(
        docstring.content.split("\n"), GOOGLE_SECTION_NAMES
    ):
        yield from _check_google_section(node, docstring, context)


@check(NODES_TO_CHECK)
def check_docstring_sections(
    node: CHECKED_NODE_TYPE, docstring: Docstring, _: Configuration
) -> Generator:
    """Check for docstring sections."""
    lines = docstring.content.split("\n")
    if len(lines) < 2:
        return

    found_numpy = yield from _check_numpy_sections(node, docstring)

    if not found_numpy:
        yield from _check_google_sections(node, docstring)

"""Contains a docstring class."""

import linecache
import re
from textwrap import dedent
from typing import Dict, List, Optional, Set, Tuple

from pydantic import BaseModel

from lintel import (
    CHECKED_NODE_TYPES,
    Configuration,
    Convention,
    has_content,
    is_blank,
    leading_space,
    pairwise,
)


class SectionUnderline(BaseModel):
    line: str
    i_line: int


class Section(BaseModel):
    """Holds information about a docstring section.

    * Section Name
    * String value of the previous line
    * The section line
    * Following lines till the next section
    * Line index of the beginning of the section in the docstring
    * Boolean indicating whether the section is the last section.
    + Optional tuple containing the line index of an underline and the underline
    """

    name: str
    previous_line: str
    line: str
    following_lines: List[str]
    underline: Optional[SectionUnderline] = None
    content_lines: List[str] = []
    i_line: int
    is_last_section: bool


class Docstring:
    """A docstring representation."""

    def __init__(self, parent_node: CHECKED_NODE_TYPES, convention: Convention):
        """Initialize the docstring.

        Args:
            parent_node: The node that the docstring is attached to.

        Raises:
            ValueError: If the parent node does not have a doc node.
        """
        if parent_node.doc_node is None:
            raise ValueError(f"Node '{parent_node.name}' does not have a doc node.")

        self.parent_node = parent_node
        self.node = parent_node.doc_node
        self.convention = convention
        self._sections: List[Section] = []

        self._parameters: List[str] = []

        self._parse_sections()
        self._parse_parameters()

    @property
    def content(self) -> str:
        """The docstring content."""
        return str(self.node.value).expandtabs()

    @property
    def raw(self) -> str:
        """The raw docstring lines."""
        return "\n".join(
            l.rstrip()
            for l in linecache.getlines(self.parent_node.root().file)[
                self.node.fromlineno - 1 : self.node.end_lineno
            ]
        )

    @property
    def lines(self) -> List[str]:
        """The lines of the docstring without triple quotes."""
        return self.content.splitlines()

    @property
    def indent(self) -> str:
        """The indentation used for the first line of the docstring."""
        # Get the text before the quotation marks on the first line of the docstring
        pre_text = re.findall("(.*?)[uU]?[rR]?(\"\"\"|\'\'\')", self.raw.splitlines()[0])[0][0]

        return "".join(' ' for _ in pre_text)

    @property
    def line_indents(self) -> List[str]:
        """The indentation of non-empty lines in the docstring."""
        lines = [
            next_line
            for first_line, next_line in pairwise(self.raw.split("\n"), "")
            if has_content(next_line) and not first_line.endswith("\\")
        ]

        line_indents = [leading_space(l) for l in lines]

        return line_indents

    def __repr__(self) -> str:
        return f'"""{self.content}"""'

    @property
    def sections(self) -> List[Section]:
        return self._sections

    @property
    def parameters(self) -> List[str]:
        return self._parameters

    def _parse_sections(self) -> None:
        if self.convention not in SECTION_NAMES:
            return

        lower_section_names = [s.lower() for s in SECTION_NAMES[self.convention]]

        sections = [
            Section(
                name=_get_leading_words(line.strip()),
                previous_line=self.lines[i_line - 1],
                line=line,
                following_lines=self.lines[i_line + 1 :],
                i_line=i_line,
                is_last_section=False,
            )
            for i_line, line in enumerate(self.lines)
            if _get_leading_words(line.lower()) in lower_section_names and i_line > 0
        ]

        # Rule out false positives.
        sections = [section for section in sections if _is_docstring_section(section)]

        # Trim the `following lines` field to only reach the next section name.
        for this_section, next_section in pairwise(sections, None):
            end = -1 if next_section is None else next_section.i_line
            this_section.following_lines = self.lines[this_section.i_line + 1 : end]  # type: ignore

        # Determine section underline and content lines
        for section in sections:
            section.underline = _get_section_title_underline(section)
            section.content_lines = section.following_lines

            if section.underline:
                if section.underline.i_line + 1 < len(section.following_lines):
                    section.content_lines = section.following_lines[section.underline.i_line + 1 :]
                else:
                    section.content_lines = []

        if sections:
            sections[-1].is_last_section = True

        self._sections = sections

    def _parse_parameters(self) -> None:
        for section in self._sections:
            if section.name == "Parameters" and self.convention == Convention.NUMPY:
                self._parameters = _parse_numpy_parameters(section)

            if section.name in ("Args", "Arguments") and self.convention == Convention.GOOGLE:
                self._parameters = _parse_google_parameters(section)


def get_docstring_from_doc_node(
    node: CHECKED_NODE_TYPES,
    config: Configuration,
) -> Docstring:
    """Retrieve the docstring of an astroid node."""
    if node.doc_node is None:
        raise ValueError("Node does not have a doc node.")

    return Docstring(node, config.convention)


def _get_leading_words(line: str) -> str:
    """Return any leading set of words from `line`.

    For example, if `line` is "  Hello world!!!", returns "Hello world".
    """
    result = re.compile(r"[\w ]+").match(line.strip())
    if result is not None:
        return result.group()

    return ""


def _is_docstring_section(section: Section) -> bool:
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
    section_name_suffix = section.line.strip().lstrip(section.name.strip()).strip()

    section_suffix_is_only_colon = section_name_suffix == ':'

    this_line_looks_like_a_section_name = (
        is_blank(section_name_suffix) or section_suffix_is_only_colon
    )

    previous_line_ends_with_punctuation = section.previous_line.strip().endswith(
        (',', ';', '.', '-', '\\', '/', ']', '}', ')')
    )

    prev_line_looks_like_end_of_paragraph = (
        is_blank(section.previous_line) or previous_line_ends_with_punctuation
    )

    return this_line_looks_like_a_section_name and prev_line_looks_like_end_of_paragraph


def _get_section_title_underline(section: Section) -> Optional[SectionUnderline]:
    non_empty_following_lines = [
        (i_line, line) for i_line, line in enumerate(section.following_lines) if has_content(line)
    ]

    if len(non_empty_following_lines) > 0 and set(non_empty_following_lines[0][1].strip()) == {"-"}:
        return SectionUnderline(
            i_line=non_empty_following_lines[0][0], line=non_empty_following_lines[0][1]
        )

    return None


def _parse_numpy_parameters(section: Section) -> List[str]:
    docstring_args = []
    section_level_indent = leading_space(section.line)
    # Join line continuations, then resplit by line.
    content = '\n'.join(section.following_lines).replace('\\\n', '').split('\n')
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
            and (len(leading_space(next_line)) > len(leading_space(current_line)))
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
                docstring_args.append(parameter.strip())

    return docstring_args


def _parse_google_parameters(section: Section) -> List[str]:
    """Parse parameters from a parameter section in Google-style docstring.

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
    docstring_args = []

    # normalize leading whitespace
    if section.following_lines:
        # any lines with shorter indent than the first one should be disregarded
        first_line = section.following_lines[0]
        leading_whitespaces = first_line[: -len(first_line.lstrip())]

    args_content = dedent(
        "\n".join(
            [
                line
                for line in section.following_lines
                if line.startswith(leading_whitespaces) or line == ""
            ]
        )
    ).strip()

    args_sections: List[str] = []
    for line in args_content.splitlines(keepends=True):
        if not line[:1].isspace():
            # This line is the start of documentation for the next
            # parameter because it doesn't start with any whitespace.
            args_sections.append(line)
        else:
            # This is a continuation of documentation for the last
            # parameter because it does start with whitespace.
            args_sections[-1] += line

    for args_section in args_sections:
        match = GOOGLE_ARGS_REGEX.match(args_section)
        if match:
            docstring_args.append(match.group(1))

    return docstring_args


SECTION_NAMES: Dict[Convention, Set[str]] = {
    Convention.NUMPY: {
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
    },
    Convention.GOOGLE: {
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
    },
}

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

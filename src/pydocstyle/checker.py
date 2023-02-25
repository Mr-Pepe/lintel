"""Parsed source code checkers for docstring violations."""

import ast
import re
import string
import tokenize as tk
from collections import namedtuple
from itertools import chain, takewhile
from pathlib import Path
from textwrap import dedent
from typing import Generator, Optional, Tuple

import astroid

import pydocstyle.checks
from pydocstyle.checks import Check, check
from pydocstyle.conventions import Convention
from pydocstyle.docstring import Docstring, docstringify
from pydocstyle.logging import log
from pydocstyle.violations import Error

from . import violations
from .config import Configuration, IllegalConfiguration
from .utils import (
    NODES_TO_CHECK,
    get_decorator_names,
    get_indents,
    get_line_noqa,
    is_blank,
    leading_space,
    pairwise,
    source_has_noqa,
)

__all__ = ('check',)


class ConventionChecker:
    """Checker for PEP 257, NumPy and Google conventions.

    D10x: Missing docstrings
    D20x: Whitespace issues
    D30x: Docstring formatting
    D40x: Docstring content issues

    """

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

    def check_source(
        self,
        filename: Path,
        source: str,
        config: Configuration = Configuration(),
    ) -> Generator:
        if source_has_noqa(source):
            return

        module = astroid.parse(
            source, module_name=filename.stem, path=filename.as_posix()
        )

        nodes = [module]

        while len(nodes) > 0:
            node = nodes.pop()

            child_nodes = list(node.get_children())

            for child_node in child_nodes:
                if isinstance(child_node, NODES_TO_CHECK):
                    nodes.append(child_node)

            error_codes_to_skip = get_line_noqa(
                node.as_string().splitlines()[0]
            )

            if "all" in error_codes_to_skip:
                continue

            decorator_names = get_decorator_names(node)

            if config.ignore_decorators is not None and any(
                len(config.ignore_decorators.findall(decorator_name)) > 0
                for decorator_name in decorator_names
            ):
                continue

            for this_check in self.checks:
                terminate = False

                if (
                    node.doc_node is None
                    and this_check.only_if_docstring_exists
                ):
                    continue

                if (
                    node.doc_node == ""
                    and this_check.only_if_docstring_not_empty
                ):
                    continue

                if not isinstance(node, this_check._node_type):
                    continue

                docstring: Optional[Docstring] = None
                if node.doc_node is not None:
                    docstring = docstringify(node.doc_node.value)

                error = None

                # TODO: Remove try clause when all checks have been extracted
                try:
                    error = this_check(self, node, docstring, config)
                except TypeError:
                    error = this_check(node, docstring, config)

                errors: list[Error] = (
                    error if hasattr(error, '__iter__') else [error]
                )

                for error in errors:
                    if error is not None and (
                        config.ignore_inline_noqa
                        or error.code not in error_codes_to_skip
                    ):
                        partition = this_check.explanation.partition('.\n')
                        message, _, explanation = partition
                        error.set_context(explanation=explanation, node=node)
                        yield error
                        if this_check._terminal:
                            terminate = True
                            break
                if terminate:
                    break

    @property
    def checks(self):
        all = [
            this_check
            for this_check in chain(
                vars(type(self)).values(),
                (
                    getattr(pydocstyle.checks, x)
                    for x in dir(pydocstyle.checks)
                ),
            )
            if isinstance(this_check, Check)
        ]
        return sorted(all, key=lambda this_check: not this_check._terminal)


def check_files(
    filenames: Tuple[str], config: Configuration = Configuration()
) -> Generator:
    """Generate docstring errors that exist in `filenames` iterable.

    By default, the PEP-257 convention is checked. To specifically define the
    set of error codes to check for, supply either `select` or `ignore` (but
    not both). In either case, the parameter should be a collection of error
    code strings, e.g., {'D100', 'D404'}.
    """
    if config.select is not None and config.ignore is not None:
        raise IllegalConfiguration(
            'Cannot pass both select and ignore. '
            'They are mutually exclusive.'
        )
    elif config.select is not None:
        checked_codes = config.select
    elif config.ignore is not None:
        checked_codes = set(violations.ErrorRegistry.get_error_codes()) - set(
            config.ignore
        )

    else:
        checked_codes = Convention().error_codes

    for filename in filenames:
        log.info('Checking file %s.', filename)
        try:
            with tk.open(filename) as file:
                source = file.read()
            for error in ConventionChecker().check_source(
                Path(filename),
                source,
                config,
            ):
                code = getattr(error, 'code', None)
                if code in checked_codes:
                    yield error
        except OSError as error:
            log.warning('Error in file %s: %s', filename, error)
            yield error
        except tk.TokenError:
            yield SyntaxError('invalid syntax in file %s' % filename)


def is_ascii(string):
    """Return a boolean indicating if `string` only has ascii characters."""
    return all(ord(char) < 128 for char in string)


def get_leading_words(line):
    """Return any leading set of words from `line`.

    For example, if `line` is "  Hello world!!!", returns "Hello world".
    """
    result = re.compile(r"[\w ]+").match(line.strip())
    if result is not None:
        return result.group()


def is_def_arg_private(arg_name):
    """Return a boolean indicating if the argument name is private."""
    return arg_name.startswith("_")


def get_function_args(function_source):
    """Return the function arguments given the source-code string."""
    # We are stripping the whitespace from the left of the
    # function source.
    # This is so that if the docstring has incorrectly
    # indented lines, which are at a lower indent than the
    # function source, we still dedent the source correctly
    # and the AST parser doesn't throw an error.
    try:
        function_arg_node = ast.parse(function_source.lstrip()).body[0].args
    except SyntaxError:
        # If we still get a syntax error, we don't want the
        # the checker to crash. Instead we just return a blank list.
        return []
    arg_nodes = function_arg_node.args
    kwonly_arg_nodes = function_arg_node.kwonlyargs
    return [arg_node.arg for arg_node in chain(arg_nodes, kwonly_arg_nodes)]

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
from pydocstyle.docstring import Docstring, get_docstring_from_doc_node
from pydocstyle.logging import log
from pydocstyle.violations import Error

from . import violations
from .config import Configuration, IllegalConfiguration
from .utils import NODES_TO_CHECK, get_decorator_names, get_error_codes_to_skip

__all__ = ('check',)


class ConventionChecker:
    """Checker for Sphinx, NumPy and Google docstrings."""

    def check_source(
        self,
        filename: Path,
        source: str,
        config: Configuration = Configuration(),
    ) -> Generator:
        module = astroid.parse(
            source, module_name=filename.stem, path=filename.as_posix()
        )

        module_wide_skipped_errors = get_error_codes_to_skip(module)

        nodes = [module]

        while len(nodes) > 0:
            node = nodes.pop()

            child_nodes = list(node.get_children())

            for child_node in child_nodes:
                if isinstance(child_node, NODES_TO_CHECK):
                    nodes.append(child_node)

            error_codes_to_skip = module_wide_skipped_errors.union(
                get_error_codes_to_skip(node)
            )

            if "all" in error_codes_to_skip:
                continue

            decorator_names = get_decorator_names(node)

            if config.ignore_decorators is not None and any(
                len(config.ignore_decorators.findall(decorator_name)) > 0
                for decorator_name in decorator_names
            ):
                continue

            docstring = get_docstring_from_doc_node(node)

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

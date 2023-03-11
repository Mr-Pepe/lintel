"""Parsed source code checkers for docstring violations."""

from pathlib import Path
from typing import Generator, List

import astroid
from astroid.exceptions import AstroidSyntaxError

import pydocstyle
from pydocstyle import violations
from pydocstyle.checks import Check
from pydocstyle.config import Configuration, IllegalConfiguration
from pydocstyle.conventions import Convention
from pydocstyle.docstring import get_docstring_from_doc_node
from pydocstyle.utils import (
    NODES_TO_CHECK,
    get_decorator_names,
    get_error_codes_to_skip,
)
from pydocstyle.violations import Error


def check_source(
    file_path: Path,
    config: Configuration = Configuration(),
) -> Generator:
    """Check a Python source file for docstring errors.

    Args:
        file_path: Path to the Python file.
        config: The configuration to use for error checking.
            Defaults to Configuration().

    Raises:
        IllegalConfiguration: If the configuration is invalid.

    Yields:
        AstroidSyntaxError: If the Python file can not be parsed.
        Error: If docstring errors are found.
    """
    if config.select is not None and config.ignore is not None:
        raise IllegalConfiguration(
            'Cannot pass both select and ignore. '
            'They are mutually exclusive.'
        )
    elif config.select is not None:
        checked_codes_base = config.select
    elif config.ignore is not None:
        checked_codes_base = set(
            violations.ErrorRegistry.get_error_codes()
        ) - set(config.ignore)
    else:
        checked_codes_base = Convention().error_codes

    with open(file_path, mode="r", encoding="utf-8") as file:
        source = file.read()

        try:
            module = astroid.parse(
                source, module_name=file_path.stem, path=file_path.as_posix()
            )
        except AstroidSyntaxError as parsing_error:
            yield parsing_error
            return

    module_wide_skipped_errors = get_error_codes_to_skip(module)

    nodes = [module]

    while len(nodes) > 0:
        node = nodes.pop()

        child_nodes = list(node.get_children())

        for child_node in child_nodes:
            if isinstance(child_node, NODES_TO_CHECK):
                nodes.append(child_node)

        error_codes_to_skip = (
            module_wide_skipped_errors | get_error_codes_to_skip(node)
        )

        if "all" in error_codes_to_skip:
            continue

        checked_codes = checked_codes_base - error_codes_to_skip

        decorator_names = get_decorator_names(node)

        if config.ignore_decorators is not None and any(
            len(config.ignore_decorators.findall(decorator_name)) > 0
            for decorator_name in decorator_names
        ):
            continue

        docstring = get_docstring_from_doc_node(node)

        for this_check in _get_checks():
            terminate = False

            if node.doc_node is None and this_check.only_if_docstring_exists:
                continue

            if (
                docstring
                and docstring.content == ""
                and this_check.only_if_docstring_not_empty
            ):
                continue

            if not isinstance(node, this_check._node_type):
                continue

            error = this_check(node, docstring, config)

            errors: List[Error] = (
                error if hasattr(error, '__iter__') else [error]
            )

            for error in errors:
                if error is not None and (
                    config.ignore_inline_noqa or error.code in checked_codes
                ):
                    partition = this_check.explanation.partition('.\n')
                    _, _, explanation = partition
                    error.set_context(explanation=explanation, node=node)
                    yield error
                    if this_check._terminal:
                        terminate = True
                        break
            if terminate:
                break


def _get_checks():
    checks = [
        this_check
        for this_check in [
            getattr(pydocstyle.checks, x) for x in dir(pydocstyle.checks)
        ]
        if isinstance(this_check, Check)
    ]
    return sorted(checks, key=lambda this_check: not this_check._terminal)

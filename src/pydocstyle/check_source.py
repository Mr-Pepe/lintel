"""Parsed source code checkers for docstring violations."""

from pathlib import Path
from typing import Generator, List, Set

import astroid
from astroid import Module
from astroid.exceptions import AstroidSyntaxError

import pydocstyle
from pydocstyle import violations
from pydocstyle.checks import Check
from pydocstyle.config import Configuration, IllegalConfiguration
from pydocstyle.conventions import Convention
from pydocstyle.docstring import Docstring, get_docstring_from_doc_node
from pydocstyle.utils import (
    CHECKED_NODE_TYPE,
    NODES_TO_CHECK,
    get_decorator_names,
    get_error_codes_to_skip,
)
from pydocstyle.violations import Error


def check_source(
    file_path: Path,
    config: Configuration = Configuration(),
) -> Generator[Error, None, AstroidSyntaxError]:
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
    codes_to_check_base = _get_codes_to_check(config)
    module = _parse_file(file_path)
    module_wide_skipped_errors = get_error_codes_to_skip(module)

    nodes = [module]

    while len(nodes) > 0:
        node = nodes.pop()

        nodes.extend(_get_child_nodes_to_check(node))

        if _skip_node(node, config):
            continue

        error_codes_to_skip = (
            module_wide_skipped_errors | get_error_codes_to_skip(node)
        )

        if "all" in error_codes_to_skip:
            continue

        codes_to_check = codes_to_check_base - error_codes_to_skip

        docstring = get_docstring_from_doc_node(node)

        terminate = False

        for this_check in _get_checks():
            if _skip_check(node, docstring, this_check):
                continue

            error = this_check(node, docstring, config)

            errors: List[Error] = (
                error if hasattr(error, '__iter__') else [error]
            )

            for error in errors:
                if error is not None and (
                    config.ignore_inline_noqa or error.code in codes_to_check
                ):
                    _, _, explanation = this_check.explanation.partition('.\n')

                    error.set_context(explanation=explanation, node=node)

                    yield error

                    if this_check.terminal:
                        terminate = True
                        break

            if terminate:
                break


def _parse_file(file_path: Path) -> Module:
    with open(file_path, mode="r", encoding="utf-8") as file:
        source = file.read()

    return astroid.parse(
        source, module_name=file_path.stem, path=file_path.as_posix()
    )


def _get_codes_to_check(config: Configuration) -> Set[str]:
    if config.select is not None and config.ignore is not None:
        raise IllegalConfiguration(
            'Cannot pass both select and ignore. '
            'They are mutually exclusive.'
        )

    if config.select is not None:
        codes_to_check = config.select

    elif config.ignore is not None:
        codes_to_check = set(violations.ErrorRegistry.get_error_codes()) - set(
            config.ignore
        )

    else:
        codes_to_check = Convention().error_codes

    return codes_to_check


def _get_child_nodes_to_check(
    node: CHECKED_NODE_TYPE,
) -> List[CHECKED_NODE_TYPE]:
    return [
        child_node
        for child_node in list(node.get_children())
        if isinstance(child_node, NODES_TO_CHECK)
    ]


def _skip_node(node: CHECKED_NODE_TYPE, config: Configuration) -> bool:
    decorator_names = get_decorator_names(node)

    if config.ignore_decorators is not None and any(
        len(config.ignore_decorators.findall(decorator_name)) > 0
        for decorator_name in decorator_names
    ):
        return True

    return False


def _get_checks():
    checks = [
        this_check
        for this_check in [
            getattr(pydocstyle.checks, x) for x in dir(pydocstyle.checks)
        ]
        if isinstance(this_check, Check)
    ]
    return sorted(checks, key=lambda this_check: not this_check.terminal)


def _skip_check(
    node: CHECKED_NODE_TYPE, docstring: Docstring, check: Check
) -> bool:
    if node.doc_node is None and check.only_if_docstring_exists:
        return True

    if (
        docstring
        and docstring.content == ""
        and check.only_if_docstring_not_empty
    ):
        return True

    if not isinstance(node, check.node_type):
        return True

    return False

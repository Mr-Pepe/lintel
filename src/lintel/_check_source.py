"""Parsed source code checkers for docstring violations."""

import re
from pathlib import Path
from typing import List

import astroid
from astroid import Module

from lintel import (
    CHECKED_NODE_TYPES,
    NODES_TO_CHECK,
    Configuration,
    DocstringError,
    get_checks,
    get_decorator_names,
    get_error_codes,
    get_error_codes_to_skip,
)


def check_source(
    file_path: Path,
    config: Configuration = Configuration(),
) -> List[DocstringError]:
    """Check a Python source file for docstring errors.

    Args:
        file_path: Path to the Python file.
        config: The configuration to use for error checking.
            Defaults to Configuration().
    """
    codes_to_check_base = get_error_codes(config)
    module = _parse_file(file_path)
    module_wide_skipped_errors = get_error_codes_to_skip(module)

    errors: List[DocstringError] = []

    nodes = [module]

    while len(nodes) > 0:
        node = nodes.pop()

        nodes.extend(_get_child_nodes_to_check(node))

        if _skip_node(node, config):
            continue

        inline_skipped_errors = get_error_codes_to_skip(node, config.ignore_inline_noqa)

        codes_to_check = codes_to_check_base - module_wide_skipped_errors - inline_skipped_errors

        for check in get_checks():
            if check.error_code() in codes_to_check:
                found_errors = check.check(node, config)

                errors.extend(found_errors)

                if found_errors and check.terminal:
                    break

    return errors


def _parse_file(file_path: Path) -> Module:
    with open(file_path, mode="r", encoding="utf-8") as file:
        source = file.read()

    return astroid.parse(source, module_name=file_path.stem, path=file_path.as_posix())


def _get_child_nodes_to_check(
    node: CHECKED_NODE_TYPES,
) -> List[CHECKED_NODE_TYPES]:
    return [
        child_node
        for child_node in list(node.get_children())
        if isinstance(child_node, NODES_TO_CHECK)
    ]


def _skip_node(node: CHECKED_NODE_TYPES, config: Configuration) -> bool:
    """Skip node if it has a decorator that should be ignored."""
    decorator_names = get_decorator_names(node)

    if config.ignore_decorators is not None and any(
        len(re.compile(config.ignore_decorators).findall(decorator_name)) > 0
        for decorator_name in decorator_names
    ):
        return True

    return False

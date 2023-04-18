"""Parsed source code checkers for docstring violations."""

from pathlib import Path
from typing import Generator, List, Set

import astroid
from astroid import Module
from astroid.exceptions import AstroidSyntaxError

from pydocstyle import (
    CHECKED_NODE_TYPES,
    NODES_TO_CHECK,
    Configuration,
    DocstringError,
    IllegalConfiguration,
    _docstring_error,
    get_checks,
    get_decorator_names,
    get_docstring_from_doc_node,
    get_error_codes,
    get_error_codes_to_skip,
)
from pydocstyle.conventions import Convention


def check_source(
    file_path: Path,
    config: Configuration = Configuration(),
) -> Generator[DocstringError, None, AstroidSyntaxError]:
    """Check a Python source file for docstring errors.

    Args:
        file_path: Path to the Python file.
        config: The configuration to use for error checking.
            Defaults to Configuration().

    Raises:
        IllegalConfiguration: If the configuration is invalid.

    Yields:
        AstroidSyntaxError: If the Python file can not be parsed.
        DocstringError: If docstring errors are found.
    """
    codes_to_check_base = _get_codes_to_check(config)
    module = _parse_file(file_path)
    module_wide_skipped_errors = get_error_codes_to_skip(module, config)

    if "all" in module_wide_skipped_errors:
        return

    nodes = [module]

    while len(nodes) > 0:
        node = nodes.pop()

        nodes.extend(_get_child_nodes_to_check(node))

        if _skip_node(node, config):
            continue

        error_codes_to_skip = module_wide_skipped_errors | get_error_codes_to_skip(node, config)

        if "all" in error_codes_to_skip:
            continue

        codes_to_check = codes_to_check_base - error_codes_to_skip

        for check in get_checks():
            if check.error_code() in codes_to_check:
                try:
                    check.check(node, config)
                except DocstringError as error:
                    # _, _, explanation = check.explanation.partition('.\n')

                    # check.set_context(explanation=explanation, node=node)

                    yield error

                    if check.terminal:
                        break


def _parse_file(file_path: Path) -> Module:
    with open(file_path, mode="r", encoding="utf-8") as file:
        source = file.read()

    return astroid.parse(source, module_name=file_path.stem, path=file_path.as_posix())


def _get_codes_to_check(config: Configuration) -> Set[str]:
    if config.select is not None and config.ignore is not None:
        raise IllegalConfiguration(
            'Cannot pass both select and ignore. ' 'They are mutually exclusive.'
        )

    if config.select is not None:
        codes_to_check = config.select

    elif config.ignore is not None:
        codes_to_check = set(get_error_codes()) - set(config.ignore)

    else:
        codes_to_check = Convention().error_codes

    return codes_to_check


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
        len(config.ignore_decorators.findall(decorator_name)) > 0
        for decorator_name in decorator_names
    ):
        return True

    return False

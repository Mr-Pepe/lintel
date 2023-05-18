import logging
import re
from typing import Set, Union

from astroid import ClassDef, FunctionDef, Module

from lintel import CHECKED_NODE_TYPES, CONVENTION_ERRORS, Configuration, Convention, get_checks

_logger = logging.getLogger(__name__)


def get_all_error_codes() -> Set[str]:
    return {check.error_code() for check in get_checks()}


def get_error_codes(config: Configuration) -> Set[str]:
    """Return the error codes applicable according to the provided configuration."""
    all_error_codes = get_all_error_codes()

    error_codes: Set[str] = all_error_codes if config.convention == Convention.ALL else set()

    for error_code in (
        CONVENTION_ERRORS.get(config.convention, set()) | config.select | config.add_select
    ):
        if error_code not in all_error_codes:
            message = (
                f"Error code '{error_code}' is selected explicitly or by the convention "
                f"'{config.convention.value}' but no check is registered for it."
            )
            _logger.error(message)
            raise ValueError(message)

        error_codes.add(error_code)

    for error_code in config.ignore | config.add_ignore:
        if error_code not in all_error_codes:
            message = (
                f"Error code '{error_code}' is unnecessarily ignored. No such check is registered."
            )
            _logger.error(message)
            raise ValueError(message)

        try:
            error_codes.remove(error_code)
        except KeyError:
            pass

    return error_codes


def get_error_codes_to_skip(node: CHECKED_NODE_TYPES, ignore_inline_noqa: bool = False) -> Set[str]:
    """Return the error codes to skip for the given node."""
    # Check for inline ignores
    if isinstance(node, (FunctionDef, ClassDef)) and not ignore_inline_noqa:
        return get_line_noqa(_get_definition_line(node))

    error_codes_to_skip: Set[str] = set()

    # Check for noqa comments in module
    if isinstance(node, Module):
        ignore_all_regex = re.compile(r"^\s*#\s*lintel\s*:\s*noqa\s*$")
        specific_ignore_regex = re.compile(r"^\s*#\s*noqa\s*:[\sA-Z\d,]*D\d+")

        for line in node.file_bytes.decode().splitlines():
            if ignore_all_regex.search(line):
                return get_all_error_codes()

            for match in specific_ignore_regex.findall(line):
                for error_code in re.findall(r"D\d{0,3}\b", match):
                    error_codes_to_skip.add(error_code)

    return error_codes_to_skip


def get_line_noqa(line: str) -> Set[str]:
    ignore_all_regex = re.compile(r".*#\s*noqa(\s*$|\s*#)")
    specific_ignore_regex = re.compile(r".*#\s*noqa\s*:\s*([\sA-Z\d,]*D\d+)")

    if ignore_all_regex.search(line):
        return get_all_error_codes()

    error_codes_to_skip: Set[str] = set()

    for match in specific_ignore_regex.findall(line):
        for error_code in re.findall(r"D\d{0,3}\b", match):
            error_codes_to_skip.add(error_code)

    return error_codes_to_skip


def _get_definition_line(node: Union[FunctionDef, ClassDef]) -> str:
    lines = node.root().file_bytes.decode().splitlines()[node.lineno - 1 : node.end_lineno]
    for line in lines:
        if line.lstrip().startswith(("def", "async def", "class")):
            return line

    raise ValueError(f"'{node.name}' does not contain a definition line.")

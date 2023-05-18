"""Command line interface for lintel."""
import logging
import os
from pathlib import Path
from typing import List, Optional

from astroid.exceptions import AstroidSyntaxError
from rich import print
from rich.console import Console
from rich.logging import RichHandler
from typer import Abort, Argument, Exit, Option, Typer
from typing_extensions import Annotated

from lintel import (
    DEFAULT_MATCH,
    DEFAULT_MATCH_DIR,
    DEFAULT_PROPERTY_DECORATORS,
    Convention,
    IllegalConfiguration,
    check_source,
    discover_files,
    load_config,
)

__all__ = ('main',)

_logger = logging.getLogger(__name__)


app = Typer()


@app.command()
def run(
    paths: Annotated[
        Optional[List[Path]],
        Argument(
            help="A list of files and directories to check.",
        ),
    ] = None,
    config_path: Annotated[
        Optional[Path],
        Option(
            "--config",
            help="A configuration file to use instead of using config discovery.",
            show_default=False,
        ),
    ] = None,
    convention: Annotated[
        Optional[Convention],
        Option(
            help=f"The convention to use. Must be one of {[c.value for c in Convention]}. "
            f"Defaults to '{Convention.DEFAULT.value}'. "
            "Add/remove error codes via the select/ignore options. "
            "The final set of error codes is determined by taking the error codes defined by the "
            "convention, then adding the error codes specified by the --select option and then "
            "removing error codes specified by the --ignore option.",
            show_default=False,
        ),
    ] = None,
    select: Annotated[
        Optional[str],
        Option(
            help="A comma-separated list of error codes to check for. "
            "The specified error codes will be added to the selected convention. "
            f"Use the {Convention.NONE.value!r} convention to only check for the error codes "
            "specified here.",
            show_default=False,
        ),
    ] = None,
    ignore: Annotated[
        Optional[str],
        Option(
            help="A comma-separated list of error codes to ignore. "
            "The specified error codes will be removed from the selected convention. "
            f"Use the {Convention.ALL.value!r} convention to select all error codes "
            "and exclude specific error codes here.",
            show_default=False,
        ),
    ] = None,
    add_select: Annotated[
        Optional[str],
        Option(
            help="A comma-separated list of error codes to check for. "
            "The specified error codes will be added to the selected convention and the error codes "
            "specified by the --select option. "
            "This option is not very useful in configuration files but allows adding error codes via "
            "the CLI in addition to the ones specified in a configuration file.",
            show_default=False,
        ),
    ] = None,
    add_ignore: Annotated[
        Optional[str],
        Option(
            help="A comma-separated list of error codes to ignore. "
            "The specified error codes will be removed from the selected convention in addition to the "
            "error codes specified by the --ignore option. "
            "This option is not very useful in configuration files but allows ignoring error codes via "
            "the CLI in addition to the ones specified in a configuration file.",
            show_default=False,
        ),
    ] = None,
    match: Annotated[
        Optional[str],
        Option(
            help="Check only files that exactly match this regular expression. "
            f"Defaults to {DEFAULT_MATCH!r} which matches Python files that don't start with 'test_'.",
            show_default=False,
        ),
    ] = None,
    match_dir: Annotated[
        Optional[str],
        Option(
            help="Search only directories that exactly match this regular expression. "
            f"Defaults to {DEFAULT_MATCH_DIR!r} which matches all directories that don't start with a dot.",
            show_default=False,
        ),
    ] = None,
    ignore_decorators: Annotated[
        Optional[str],
        Option(
            help="Ignore any functions or methods that are decorated "
            "by a function with a name matching this regular expression. "
            "The default does not ignore any decorated functions.",
            show_default=False,
        ),
    ] = None,
    property_decorators: Annotated[
        Optional[str],
        Option(
            help="A comma-separated list of property decorators. "
            "Consider any method decorated with one of these "
            "decorators as a property and consequently allow "
            "a docstring which is not in imperative mood. "
            f"Defaults to {list(DEFAULT_PROPERTY_DECORATORS)}.",
            show_default=False,
        ),
    ] = None,
    ignore_inline_noqa: Annotated[
        Optional[bool],
        Option(
            help="Whether inline `# noqa` comments are respected or not.",
            show_default=False,
        ),
    ] = None,
    verbose: Annotated[
        Optional[bool],
        Option(
            help="Whether to show more detailed output.",
            show_default=False,
        ),
    ] = None,
) -> None:
    """Check docstring style.

    Options passed via the CLI take precedence over values set in a configuration file.
    """
    configure_logging(verbose or False)

    paths = paths or [Path().cwd()]

    try:
        config_path = config_path or paths[0] if paths and paths[0].is_dir() else None
        config_path = config_path or Path().cwd()
        config = load_config(config_path or Path().cwd())
    except IllegalConfiguration as config_error:
        _logger.error(config_error)
        raise Exit(1)

    config.convention = convention or config.convention
    config.select = set(select.split(",")) if select else config.select
    config.ignore = set(ignore.split(",")) if ignore else config.ignore
    config.add_select = set(add_select.split(",")) if add_select else config.add_select
    config.add_ignore = set(add_ignore.split(",")) if add_ignore else config.add_ignore
    config.match = match or config.match
    config.match_dir = match_dir or config.match_dir
    config.ignore_decorators = ignore_decorators or config.ignore_decorators
    config.property_decorators = (
        set(property_decorators.split(",")) if property_decorators else config.property_decorators
    )
    config.ignore_inline_noqa = ignore_inline_noqa or config.ignore_inline_noqa
    config.verbose = verbose or config.verbose

    # Reconfigure logging with the configured verbosity level
    configure_logging(config.verbose)

    _logger.info(f"Using configuration: {config}")

    exit_code = 0
    error_count = 0

    files_to_check = discover_files(paths, config)

    for filename in files_to_check:
        _logger.info("Checking file: %s" % filename)

        try:
            for error in check_source(Path(filename), config):
                _logger.error(error)
                exit_code = 1
                error_count += 1

        except AstroidSyntaxError:
            _logger.error(f"{filename}: Cannot parse file")
            exit_code = 1

    n_checked_files = len(files_to_check)

    if error_count > 0:
        print()

    print(
        f"{'💥' if error_count> 0 else '🚀'} "
        f"Found {error_count} error{'s' if error_count > 1  or error_count == 0 else ''} "
        f"in {n_checked_files} file{'s' if n_checked_files > 1 or n_checked_files == 0 else ''}."
    )

    raise Exit(exit_code)


def configure_logging(verbose: bool) -> None:
    """Set up logging."""
    stdout_handler = RichHandler(
        console=Console(
            width=500 if "LINTEL_TESTING" in os.environ else None,
        ),
        rich_tracebacks=True,
        show_time=False,
        show_path=False,
    )
    stdout_handler.setFormatter(logging.Formatter("%(message)s"))

    stderr_handler = RichHandler(
        console=Console(
            stderr=True, quiet=True, width=500 if "LINTEL_TESTING" in os.environ else None
        ),
        level=logging.WARNING,
        rich_tracebacks=True,
        show_time=False,
        show_path=False,
    )
    stderr_handler.setFormatter(logging.Formatter("%(message)s"))

    logging.getLogger("lintel").setLevel(logging.DEBUG if verbose else logging.WARNING)
    logging.getLogger("lintel").handlers = [stdout_handler, stderr_handler]

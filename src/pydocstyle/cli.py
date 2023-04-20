"""Command line interface for pydocstyle."""
import logging
import sys
from pathlib import Path
from typing import Optional

from astroid.exceptions import AstroidSyntaxError
from rich.logging import RichHandler
from typer import Exit, Option, Typer

from pydocstyle import Configuration, Convention, IllegalConfiguration, check_source, load_config

__all__ = ('main',)

_logger = logging.getLogger(__name__)


app = Typer(rich_help_panel=True)


class ReturnCode:
    no_violations_found = 0
    violations_found = 1
    invalid_options = 2


@app.command()
def run(
    config_path: Optional[Path] = Option(
        None,
        "--config",
        help="A configuration file to use instead of using config discovery.",
        show_default=False,
    ),
    convention: str = Option(
        Convention.PEP257.value,
        help=f"The convention to use. Must be one of {[c.value for c in Convention]}. "
        "Add/remove error codes via the select/ignore options. "
        "The final set of error codes is determined by taking the error codes defined by the "
        "convention, then adding the error codes specified by the --select option and then "
        "removing error codes specified by the --ignore option.",
    ),
    select: str = Option(
        "",
        help="A comma-separated list of error codes to check for. "
        "The specified error codes will be added to the selected convention. "
        f"Use the {Convention.NONE.value!r} convention to only check for the error codes "
        "specified here.",
    ),
    ignore: str = Option(
        "",
        help="A comma-separated list of error codes to ignore. "
        "The specified error codes will be removed from the selected convention. "
        f"Use the {Convention.ALL.value!r} convention to select all error codes "
        "and exclude specific error codes here.",
    ),
    match: Optional[str] = Option(
        None,
        help="Check only files that exactly match this regular expression. "
        "The default matches Python files that don't start with 'test_'.",
        show_default=False,
    ),
    match_dir: Optional[str] = Option(
        None,
        help="Search only directories that exactly match this regular expression. "
        "The default matches all directories that don't start with a dot.",
        show_default=False,
    ),
    ignore_decorators: Optional[str] = Option(
        None,
        help="Ignore any functions or methods that are decorated "
        "by a function with a name matching this regular expression. "
        "The default  does not ignore any decorated functions.",
        show_default=False,
    ),
    property_decorators: Optional[str] = Option(
        None,
        help="A comma-separated list of property decorators. "
        "Consider any method decorated with one of these "
        "decorators as a property and consequently allow "
        "a docstring which is not in imperative mood.",
        show_default=False,
    ),
    ignore_inline_noqa: Optional[bool] = Option(
        None, help="Whether inline `# noqa` comments are respected or not."
    ),
    verbose: Optional[bool] = Option(None, help="Whether to show more detailed output."),
):
    """Check docstring style."""
    configure_logging(verbose)

    config = load_config(config_path=config)
    config = ConfigurationParser()
    config.parse()

    run_conf = config.get_user_run_configuration()

    # Reset the logger according to the command line arguments
    configure_logging(run_conf)

    error_count = 0

    for filename in []:
        _logger.info("Checking file: %s" % filename)

        config = Configuration(
            select=checked_codes,
            ignore_decorators=ignore_decorators,
            property_decorators=property_decorators,
        )

        try:
            for error in check_source(Path(filename), config):
                sys.stdout.write('%s\n' % error)
                error_count += 1

        except AstroidSyntaxError:
            sys.stderr.write(f"{filename}: Cannot parse file")
            error_count += 1

    if error_count == 0:
        exit_code = ReturnCode.no_violations_found
    else:
        exit_code = ReturnCode.violations_found
    if run_conf.count:
        print(error_count)
    return exit_code


def configure_logging(verbose: bool):
    """Set up logging."""

    rich_handler = RichHandler(rich_tracebacks=True)
    rich_handler.setFormatter(logging.Formatter("%(message)s"))

    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        handlers=[rich_handler],
    )

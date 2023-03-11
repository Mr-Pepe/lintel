"""Command line interface for pydocstyle."""
import logging
import sys
from pathlib import Path

from astroid.exceptions import AstroidSyntaxError

from .checker import check_source
from .config import Configuration, ConfigurationParser, IllegalConfiguration
from .violations import Error

__all__ = ('main',)

_logger = logging.getLogger(__name__)


class ReturnCode:
    no_violations_found = 0
    violations_found = 1
    invalid_options = 2


def run_pydocstyle():
    _logger.setLevel(logging.DEBUG)
    conf = ConfigurationParser()
    setup_stream_handlers(conf.get_default_run_configuration())

    try:
        conf.parse()
    except IllegalConfiguration:
        return ReturnCode.invalid_options

    run_conf = conf.get_user_run_configuration()

    # Reset the logger according to the command line arguments
    setup_stream_handlers(run_conf)

    _logger.debug("starting in debug mode.")

    Error.explain = run_conf.explain
    Error.source = run_conf.source

    error_count = 0
    try:
        for (
            filename,
            checked_codes,
            ignore_decorators,
            property_decorators,
        ) in conf.get_files_to_check():
            _logger.info("Checking file: %s" % filename)

            config = Configuration(
                select=checked_codes,
                ignore_decorators=ignore_decorators,
                property_decorators=property_decorators,
            )
            for error in check_source(Path(filename), config):
                if hasattr(error, 'code'):
                    sys.stdout.write('%s\n' % error)

                if isinstance(error, AstroidSyntaxError):
                    sys.stderr.write(f"{filename}: Cannot parse file")

                error_count += 1
    except IllegalConfiguration as error:
        # An illegal configuration file was found during file generation.
        _logger.error(error.args[0])
        return ReturnCode.invalid_options

    if error_count == 0:
        exit_code = ReturnCode.no_violations_found
    else:
        exit_code = ReturnCode.violations_found
    if run_conf.count:
        print(error_count)
    return exit_code


def main():
    """Run pydocstyle as a script."""
    try:
        sys.exit(run_pydocstyle())
    except KeyboardInterrupt:
        pass


def setup_stream_handlers(conf):
    """Set up logging stream handlers according to the options."""

    class StdoutFilter(logging.Filter):
        def filter(self, record):
            return record.levelno in (logging.DEBUG, logging.INFO)

    _logger.handlers = []

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.WARNING)
    stdout_handler.addFilter(StdoutFilter())
    if conf.debug:
        stdout_handler.setLevel(logging.DEBUG)
    elif conf.verbose:
        stdout_handler.setLevel(logging.INFO)
    else:
        stdout_handler.setLevel(logging.WARNING)
    _logger.addHandler(stdout_handler)

    stderr_handler = logging.StreamHandler(sys.stderr)
    msg_format = "%(levelname)s: %(message)s"
    stderr_handler.setFormatter(logging.Formatter(fmt=msg_format))
    stderr_handler.setLevel(logging.WARNING)
    _logger.addHandler(stderr_handler)

"""Contains a sandbox environment to execute integration tests."""


import os
import shutil
import tempfile
from io import TextIOWrapper
from typing import Any, Optional

from click.testing import Result
from typer.testing import CliRunner

from lintel.cli import app

_runner = CliRunner(mix_stderr=False, env={"LINTEL_TESTING": "True"})


class SandboxEnv:
    """An isolated environment where lintel can be run.

    Since running lintel as a script is affected by local config files,
    it's important that tests will run in an isolated environment. This class
    should be used as a context manager and offers utility methods for adding
    files to the environment and changing the environment's configuration.

    """

    def __init__(
        self,
        script_name='lintel',
        section_name='lintel',
        config_name='tox.ini',
    ):
        """Initialize the object."""
        self.tempdir = None
        self.script_name = script_name
        self.section_name = section_name
        self.config_name = config_name

    def write_config(self, prefix='', name=None, **kwargs):
        """Change an environment config file.

        Applies changes to `tox.ini` relative to `tempdir/prefix`.
        If the given path prefix does not exist it is created.

        """
        base = os.path.join(self.tempdir, prefix) if prefix else self.tempdir
        if not os.path.isdir(base):
            self.makedirs(base)

        name = self.config_name if name is None else name
        if name.endswith('.toml'):

            def convert_value(val):
                return repr(val).lower() if isinstance(val, bool) else repr(val)

        else:

            def convert_value(val):
                return val

        with open(os.path.join(base, name), 'wt') as conf:
            conf.write(f"[{self.section_name}]\n")
            for k, v in kwargs.items():
                conf.write("{} = {}\n".format(k.replace('_', '-'), convert_value(v)))

    def open(self, path: str, *args: Any, **kwargs: Any) -> TextIOWrapper:
        """Open a file in the environment.

        The file path should be relative to the base of the environment.

        """
        return open(os.path.join(self.tempdir, path), *args, **kwargs)

    def makedirs(self, path, *args, **kwargs):
        """Create a directory in a path relative to the environment base."""
        os.makedirs(os.path.join(self.tempdir, path), *args, **kwargs)

    def invoke(self, args: str = "", target: Optional[str] = None) -> Result:
        """Run lintel on the environment base folder with the given args.

        If `target` is not None, will run lintel on `target` instead of
        the environment base folder.

        """
        run_target = self.tempdir if target is None else os.path.join(self.tempdir, target)

        return _runner.invoke(app, f'"{run_target}" {args}')

    def __enter__(self):
        self.tempdir = tempfile.mkdtemp()
        # Make sure we won't be affected by other config files
        self.write_config()
        return self

    def __exit__(self, *args, **kwargs):
        shutil.rmtree(self.tempdir)
        pass

"""Use tox or pytest to run the test-suite."""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
from tests.utils.sandbox_env import SandboxEnv
from typer.testing import CliRunner

from lintel import Configuration, Convention, check_source
from lintel.cli import app

__all__ = ()

_runner = CliRunner(mix_stderr=False)


def test_non_existent_config_path_raises_error() -> None:
    result = _runner.invoke(app, config="abcdef")

    assert result.exit_code == 1
    assert "Failed to load configuration from 'abcdef' because that path does not exist."


def test_ignore_list(tmp_path: Path) -> None:
    """Test that `ignore`d errors are not reported in the API."""
    test_file_path = tmp_path / "test.py"
    with open(test_file_path, mode="w", encoding="utf-8") as file:
        file.write(
            textwrap.dedent(
                '''
        def function_with_bad_docstring(foo):
            """ does spacing without a period in the end
            no blank line after one-liner is bad. Also this - """
            return foo
    '''
            )
        )
    expected_error_codes = {
        'D100',
        'D400',
        'D401',
        'D205',
        'D209',
        'D210',
        'D403',
        'D415',
        'D417',
        'D213',
    }

    errors = check_source(
        test_file_path,
        Configuration(convention=Convention.ALL),
    )

    error_codes = {error.error_code() for error in errors}
    assert error_codes == expected_error_codes

    ignored = {'D100', 'D213', "D415"}
    errors = check_source(
        test_file_path,
        Configuration(convention=Convention.ALL, ignore=ignored),
    )

    error_codes = {error.error_code() for error in errors}
    assert error_codes == expected_error_codes - ignored


def test_skip_errors(tmp_path: Path) -> None:
    """Test that `ignore`d errors are not reported in the API."""
    test_file_path = tmp_path / "test.py"
    with open(test_file_path, mode="w", encoding="utf-8") as file:
        file.write(
            textwrap.dedent(
                '''
        def function_with_bad_docstring(foo):  # noqa: D400, D401, D403, D415
            """ does spacing without a period in the end
            no blank line after one-liner is bad. Also this - """
            return foo
    '''
            )
        )
    expected_error_codes = {'D100', 'D205', 'D209', 'D210', 'D213', 'D417'}

    errors = tuple(
        check_source(
            test_file_path,
            Configuration(convention=Convention.ALL),
        )
    )
    error_codes = {error.error_code() for error in errors}
    assert error_codes == expected_error_codes

    skipped_error_codes = {'D400', 'D401', 'D403', 'D415'}
    errors = tuple(
        check_source(
            test_file_path,
            Configuration(convention=Convention.ALL, ignore_inline_noqa=True),
        )
    )
    error_codes = {error.error_code() for error in errors}
    assert error_codes == expected_error_codes | skipped_error_codes


def test_run_as_named_module():
    """Test that lintel can be run as a "named module".

    This means that the following should run lintel:

        python -m lintel

    """
    cmd = [sys.executable, "-m", "lintel", "--help"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    assert p.returncode == 0, out.decode('utf-8') + err.decode('utf-8')


def test_config_file(env: SandboxEnv) -> None:
    """Test that options are correctly loaded from a config file.

    This test create a temporary directory and creates two files in it: a
    Python file that has two violations (D100 and D103) and a config
    file (tox.ini). This test alternates settings in the config file and checks
    that we give the correct output.

    """
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            def foo():
                pass
        """
            )
        )

    env.write_config(ignore='D100')
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D100' not in result.stdout
    assert 'D103' in result.stdout

    env.write_config(ignore='')
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D100' in result.stdout
    assert 'D103' in result.stdout

    env.write_config(ignore='D100,D103')
    result = env.invoke()
    assert result.exit_code == 0
    assert 'D100' not in result.stdout
    assert 'D103' not in result.stdout


def test_missing_lintel_section(env: SandboxEnv) -> None:
    """Test that config files without a valid section name issue a warning."""
    with env.open('config.ini', 'wt') as conf:
        conf.write('[bla]')
        config_path = conf.name

    result = env.invoke(f'--config="{config_path}"')
    assert result.exit_code == 1
    assert f'Configuration file {config_path} does not contain a lintel section.' in result.stdout

    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            def foo():
                pass
        """
            )
        )

    with env.open('tox.ini', 'wt') as conf:
        conf.write('[bla]\n')
        conf.write('ignore = D100')

    result = env.invoke()
    assert result.exit_code == 1
    assert 'D100' in result.stdout
    assert 'does not contain a lintel section' not in result.stderr


@pytest.mark.parametrize(
    # Don't parametrize over 'pyproject.toml'
    # since this test applies only to '.ini' files
    'env',
    ['ini'],
    indirect=True,
)
def test_multiple_lined_config_file(env: SandboxEnv) -> None:
    """Test that .ini files with multi-lined entries are parsed correctly."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            class Foo(object):
                "Doc string"
                def foo():
                    pass
        """
            )
        )

    select_string = 'D100,\n' '  #D103,\n' ' D204, D300 # Just remember - don\'t check D103!'
    env.write_config(select=select_string)

    result = env.invoke()
    assert result.exit_code == 1
    assert 'D100' in result.stdout
    assert 'D204' in result.stdout
    assert 'D300' in result.stdout
    assert 'D103' not in result.stdout


@pytest.mark.parametrize(
    # Don't parametrize over 'tox.ini' since
    # this test applies only to '.toml' files
    'env',
    ['toml'],
    indirect=True,
)
def test_accepts_select_error_code_list(env: SandboxEnv) -> None:
    """Test that .ini files with multi-lined entries are parsed correctly."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            class Foo(object):
                "Doc string"
                def foo():
                    pass
        """
            )
        )

    env.write_config(select='D100,D204,D300')

    result = env.invoke()
    assert result.exit_code == 1
    assert 'D100' in result.stdout
    assert 'D204' in result.stdout
    assert 'D300' in result.stdout
    assert 'D103' not in result.stdout


def test_config_path(env: SandboxEnv) -> None:
    """Test that options are correctly loaded from a specific config file.

    Make sure that a config file passed via --config is actually used and that
    normal config file discovery is disabled.

    """
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            def foo():
                pass
        """
            )
        )

    # either my_config.ini or my_config.toml
    config_ext = env.config_name.split('.')[-1]
    config_name = 'my_config.' + config_ext

    env.write_config(ignore='D100')
    env.write_config(name=config_name, ignore='D103')

    result = env.invoke()
    assert result.exit_code == 1
    assert 'D100' not in result.stdout
    assert 'D103' in result.stdout

    result = env.invoke(f'--config="{os.path.join(env.tempdir, config_name)}"')
    assert result.exit_code == 1, result.stdout + result.stderr
    assert 'D100' in result.stdout
    assert 'D103' not in result.stdout


def test_verbose(env: SandboxEnv) -> None:
    """Test that passing --verbose prints more information."""
    with env.open('example.py', 'wt') as example:
        example.write('"""Module docstring."""\n')

    result = env.invoke()
    assert result.exit_code == 0
    assert 'example.py' not in result.stdout

    result = env.invoke(args="--verbose")
    assert result.exit_code == 0
    assert 'example.py' in result.stdout


def test_select_cli(env: SandboxEnv) -> None:
    """Test choosing error codes with `--select` in the CLI."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            def foo():
                pass
        """
            )
        )

    result = env.invoke(args="--convention=none --select=D100")
    assert result.exit_code == 1
    assert 'D100' in result.stdout
    assert 'D103' not in result.stdout


def test_select_config(env: SandboxEnv) -> None:
    """Test choosing error codes with `select` in the config file."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            class Foo(object):
                "Doc string"
                def foo():
                    pass
        """
            )
        )

    env.write_config(select="D100,D300")
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D100' in result.stdout
    assert 'D300' in result.stdout
    assert 'D103' not in result.stdout


def test_add_select_cli(env: SandboxEnv) -> None:
    """Test choosing error codes with --add-select in the CLI."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            class Foo(object):
                "Doc string"
                def foo():
                    pass
        """
            )
        )

    env.write_config(select="D100")
    result = env.invoke(args="--add-select=D204,D300")
    assert result.exit_code == 1
    assert 'D100' in result.stdout
    assert 'D204' in result.stdout
    assert 'D300' in result.stdout
    assert 'D103' not in result.stdout


def test_add_ignore_cli(env: SandboxEnv) -> None:
    """Test choosing error codes with --add-ignore in the CLI."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            class Foo(object):
                def foo():
                    pass
        """
            )
        )

    env.write_config(select="D100,D101")
    result = env.invoke(args="--add-ignore=D101")
    assert result.exit_code == 1
    assert 'D100' in result.stdout
    assert 'D101' not in result.stdout
    assert 'D103' not in result.stdout


@pytest.mark.parametrize(
    # Don't parametrize over 'tox.ini' since
    # this test applies only to '.toml' files
    'env',
    ['toml'],
    indirect=True,
)
def test_accepts_ignore_error_code_list(env: SandboxEnv) -> None:
    with env.open('example.py', 'wt') as example:
        example.write("class Foo(object):\n    'Doc string'")
    env.write_config(ignore='D100,D300')
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D300' not in result.stdout
    assert result.stderr == ''


def test_bad_wildcard_add_ignore_cli(env: SandboxEnv) -> None:
    """Test adding a non-existent error codes with --add-ignore."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            class Foo(object):
                "Doc string"
                def foo():
                    pass
        """
            )
        )

    result = env.invoke(args="--add-ignore=D3004")
    assert result.exit_code == 1
    assert (
        "Error code 'D3004' is unnecessarily ignored. No such check is registered." in result.stdout
    )


def test_overload_function(env: SandboxEnv) -> None:
    """Functions decorated with @overload trigger D418 error."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''\
        from typing import overload


        @overload
        def overloaded_func(a: int) -> str:
            ...


        @overload
        def overloaded_func(a: str) -> str:
            """Foo bar documentation."""
            ...


        def overloaded_func(a):
            """Foo bar documentation."""
            return str(a)

        '''
            )
        )
    env.write_config(ignore="D100")
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D418' in result.stdout
    assert 'D103' not in result.stdout


def test_overload_async_function(env: SandboxEnv) -> None:
    """Async functions decorated with @overload trigger D418 error."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''\
        from typing import overload


        @overload
        async def overloaded_func(a: int) -> str:
            ...


        @overload
        async def overloaded_func(a: str) -> str:
            """Foo bar documentation."""
            ...


        async def overloaded_func(a):
            """Foo bar documentation."""
            return str(a)

        '''
            )
        )
    env.write_config(ignore="D100")
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D418' in result.stdout
    assert 'D103' not in result.stdout


def test_overload_method(env: SandboxEnv) -> None:
    """Methods decorated with @overload trigger D418 error."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''\
        from typing import overload

        class ClassWithMethods:
            @overload
            def overloaded_method(a: int) -> str:
                ...


            @overload
            def overloaded_method(a: str) -> str:
                """Foo bar documentation."""
                ...


            def overloaded_method(a):
                """Foo bar documentation."""
                return str(a)

        '''
            )
        )
    env.write_config(ignore="D100")
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D418' in result.stdout
    assert 'D102' not in result.stdout
    assert 'D103' not in result.stdout


def test_overload_method_valid(env: SandboxEnv) -> None:
    """Valid case for overload decorated Methods.

    This shouldn't throw any errors.
    """
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''\
        from typing import overload

        class ClassWithMethods:
            """Valid docstring in public Class."""

            @overload
            def overloaded_method(a: int) -> str:
                ...


            @overload
            def overloaded_method(a: str) -> str:
                ...


            def overloaded_method(a):
                """Foo bar documentation."""
                return str(a)

        '''
            )
        )
    env.write_config(ignore="D100, D203")
    result = env.invoke()
    assert result.exit_code == 0


def test_overload_function_valid(env: SandboxEnv) -> None:
    """Valid case for overload decorated functions.

    This shouldn't throw any errors.
    """
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''\
        from typing import overload


        @overload
        def overloaded_func(a: int) -> str:
            ...


        @overload
        def overloaded_func(a: str) -> str:
            ...


        def overloaded_func(a):
            """Foo bar documentation."""
            return str(a)

        '''
            )
        )
    env.write_config(ignore="D100")
    result = env.invoke()
    assert result.exit_code == 0


def test_overload_async_function_valid(env: SandboxEnv) -> None:
    """Valid case for overload decorated async functions.

    This shouldn't throw any errors.
    """
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''\
        from typing import overload


        @overload
        async def overloaded_func(a: int) -> str:
            ...


        @overload
        async def overloaded_func(a: str) -> str:
            ...


        async def overloaded_func(a):
            """Foo bar documentation."""
            return str(a)

        '''
            )
        )
    env.write_config(ignore="D100")
    result = env.invoke()
    assert result.exit_code == 0


def test_overload_nested_function(env: SandboxEnv) -> None:
    """Nested functions decorated with @overload trigger D418 error."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''\
        from typing import overload

        def function_with_nesting():
            """Valid docstring in public function."""
            @overload
            def overloaded_func(a: int) -> str:
                ...


            @overload
            def overloaded_func(a: str) -> str:
                """Foo bar documentation."""
                ...


            def overloaded_func(a):
                """Foo bar documentation."""
                return str(a)
            '''
            )
        )
    env.write_config(ignore="D100")
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D418' in result.stdout
    assert 'D103' not in result.stdout


def test_overload_nested_function_valid(env: SandboxEnv) -> None:
    """Valid case for overload decorated nested functions.

    This shouldn't throw any errors.
    """
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''\
        from typing import overload

        def function_with_nesting():
            """Adding a docstring to a function."""
            @overload
            def overloaded_func(a: int) -> str:
                ...


            @overload
            def overloaded_func(a: str) -> str:
                ...


            def overloaded_func(a):
                """Foo bar documentation."""
                return str(a)
            '''
            )
        )
    env.write_config(ignore="D100")
    result = env.invoke()
    assert result.exit_code == 0


def test_default_convention(env: SandboxEnv) -> None:
    """Test that the 'default' convention has the correct errors."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''
            class Foo(object):


                """Docstring for this class"""
                def foo():
                    pass


            # Original PEP-257 example from -
            # https://www.python.org/dev/peps/pep-0257/
            def complex(real=0.0, imag=0.0):
                """Form a complex number.

                Keyword arguments:
                real -- the real part (default 0.0)
                imag -- the imaginary part (default 0.0)
                """
                if imag == 0.0 and real == 0.0:
                    return complex_zero
        '''
            )
        )

    env.write_config(convention="default")
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D100' in result.stdout
    assert 'D211' in result.stdout
    assert 'D203' not in result.stdout
    assert 'D212' not in result.stdout
    assert 'D213' not in result.stdout
    assert 'D413' not in result.stdout


def test_numpy_convention(env: SandboxEnv) -> None:
    """Test that the 'numpy' convention options has the correct errors."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''
            class Foo(object):
                """Docstring for this class.

                returns
                 ------
                """
                def __init__(self):
                    pass
        '''
            )
        )

    env.write_config(convention="numpy")
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D107' not in result.stdout
    assert 'D213' not in result.stdout
    assert 'D215' in result.stdout
    assert 'D405' in result.stdout
    assert 'D409' in result.stdout
    assert 'D414' in result.stdout
    assert 'D410' not in result.stdout
    assert 'D413' not in result.stdout


def test_google_convention(env: SandboxEnv) -> None:
    """Test that the 'google' convention options has the correct errors."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                '''
            def func(num1, num2, num3, num_three=0):
                """Docstring for this function.

                Args:
                    num1 (int): Number 1.
                    num2: Number 2.
                """


            class Foo(object):
                """Docstring for this class.

                Attributes:

                    test: Test

                returns:
                """
                def __init__(self):
                    pass
        '''
            )
        )

    env.write_config(convention="google", verbose=True)
    result = env.invoke()
    assert result.exit_code == 1
    assert 'D107' in result.stdout
    assert 'D213' not in result.stdout
    assert 'D215' not in result.stdout
    assert 'D405' in result.stdout
    assert 'D409' not in result.stdout
    assert 'D410' not in result.stdout
    assert 'D412' in result.stdout
    assert 'D413' not in result.stdout
    assert 'D414' in result.stdout
    assert 'D417' in result.stdout


def test_syntax_error_multiple_files(env: SandboxEnv) -> None:
    """Test that a syntax error in a file doesn't prevent further checking."""
    for filename in ('first.py', 'second.py'):
        with env.open(filename, 'wt') as file:
            file.write("[")

    result = env.invoke(args="--verbose")
    assert result.exit_code == 1
    assert 'first.py: Cannot parse file' in result.stdout
    assert 'second.py: Cannot parse file' in result.stdout


def test_indented_function(env: SandboxEnv) -> None:
    """Test that nested functions do not cause IndentationError."""
    with env.open("test.py", 'wt') as file:
        file.write(
            textwrap.dedent(
                '''\
            def foo():
                def bar(a):
                    """A docstring

                    Args:
                        a : An argument.
                    """
                    pass
        '''
            )
        )
    env.write_config(convention="none")
    result = env.invoke(args="--verbose")
    assert result.exit_code == 0
    assert "IndentationError: unexpected indent" not in result.stderr


def test_only_comment_file(env: SandboxEnv) -> None:
    """Test that file with only comments does only cause D100."""
    with env.open('comments.py', 'wt') as comments:
        comments.write(
            '#!/usr/bin/env python3\n'
            '# -*- coding: utf-8 -*-\n'
            '# Useless comment\n'
            '# Just another useless comment\n'
        )

    result = env.invoke()
    assert 'D100' in result.stdout
    out = result.stdout.replace('D100', '')
    for err in {'D1', 'D2', 'D3', 'D4'}:
        assert err not in out
    assert result.exit_code == 1


def test_comment_plus_docstring_file(env: SandboxEnv) -> None:
    """Test that file with comments and docstring does not cause errors."""
    with env.open('comments_plus.py', 'wt') as comments_plus:
        comments_plus.write(
            '#!/usr/bin/env python3\n'
            '# -*- coding: utf-8 -*-\n'
            '# Useless comment\n'
            '# Just another useless comment\n'
            '"""Module docstring."""\n'
        )

    result = env.invoke()
    assert result.exit_code == 0


def test_only_comment_with_noqa_file(env: SandboxEnv) -> None:
    """Test that file with noqa and only comments does not cause errors."""
    with env.open('comments.py', 'wt') as comments:
        comments.write(
            '#!/usr/bin/env python3\n'
            '# -*- coding: utf-8 -*-\n'
            '# Useless comment\n'
            '# Just another useless comment\n'
            '# lintel: noqa\n'
        )

    result = env.invoke()
    assert 'D100' not in result.stdout
    assert result.exit_code == 0


def test_comment_with_noqa_plus_docstring_file(env: SandboxEnv) -> None:
    """Test that file with comments, noqa, docstring does not cause errors."""
    with env.open('comments_plus.py', 'wt') as comments_plus:
        comments_plus.write(
            '#!/usr/bin/env python3\n'
            '# -*- coding: utf-8 -*-\n'
            '# Useless comment\n'
            '# Just another useless comment\n'
            '# lintel : noqa\n'
            '"""Module docstring without period"""\n'
        )

    result = env.invoke()
    assert result.exit_code == 0


def test_comment_with_blank_noqa_for_single_line(env: SandboxEnv) -> None:
    """Test that a blank noqa comment ignores errors for that node."""
    with env.open('example.py', 'wt') as example:
        example.write(
            textwrap.dedent(
                """\
            def foo(): # noqa
                pass
        """
            )
        )

    result = env.invoke()
    assert result.exit_code == 1
    assert 'D100' in result.stdout  # Missing module docstring is reported
    assert 'D103' not in result.stdout  # Missing function docstring is ignored


def test_match_considers_base_names_for_path_args(env: SandboxEnv) -> None:
    """Test that `match` option only considers base names for path arguments.

    The test environment consists of a single empty module `test_a.py`. The
    match option is set to a pattern that ignores test_ prefixed .py filenames.
    When lintel is invoked with full path to `test_a.py`, we expect it to
    succeed since match option will match against just the file name and not
    full path.
    """
    # Ignore .py files prefixed with 'test_'
    env.write_config(select='D100', match='(?!test_).+.py')

    # Create an empty module (violates D100)
    with env.open('test_a.py', 'wt') as test:
        test.write('')

    result = env.invoke(target='test_a.py')
    assert result.exit_code == 0


@pytest.mark.parametrize(
    ("content", "exit_code", "output"),
    [
        ("", 1, "💥 Found 1 error in 1 file.\n"),
        ('"""Docstring."""', 0, "🚀 Found 0 errors in 1 file.\n"),
    ],
)
def test_run_summary(content: str, exit_code: int, output: str, env: SandboxEnv) -> None:
    # Create an empty module (violates D100)
    with env.open('test.py', 'wt') as test:
        test.write(content)

    result = env.invoke(target='test.py')
    assert result.exit_code == exit_code
    assert result.stdout.endswith(output)

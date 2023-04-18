from tests.utils.sandbox_env import SandboxEnv


def test_missing_docstring_in_package(env: SandboxEnv) -> None:
    """Make sure __init__.py files are treated as packages."""
    with env.open('__init__.py', 'wt') as init:
        init.write("# Well hello there")

    out, err, exit_code = env.invoke()

    assert exit_code == 1
    assert 'D100' not in out  # shouldn't be treated as a module
    assert 'D104' in out  # missing docstring in package


def test_package_with_docstring_has_no_error(env: SandboxEnv) -> None:
    with env.open('__init__.py', 'wt') as package_init:
        package_init.write('"""My docstring."""\n')

    out, _, exit_code = env.invoke()

    assert exit_code == 0
    assert out == ""

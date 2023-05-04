from tests.utils.sandbox_env import SandboxEnv


def test_missing_docstring_in_module(env: SandboxEnv) -> None:
    with env.open('my_module.py', 'w', encoding="utf-8") as file:
        file.write("import os\n")

    result = env.invoke()

    assert result.exit_code == 1
    assert 'D100' in result.stdout


def test_private_module_is_ignored(env: SandboxEnv) -> None:
    with env.open('_my_module.py', 'w', encoding="utf-8") as file:
        file.write("import os\n")

    result = env.invoke()

    assert result.exit_code == 0

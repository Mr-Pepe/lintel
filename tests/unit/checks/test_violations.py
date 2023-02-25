import astroid

from pydocstyle.violations import D419


def test_str_representation() -> None:
    node = astroid.parse("def func():\n\t...")
    error = D419()
    error.set_context(explanation="", node=node)

    print(error)

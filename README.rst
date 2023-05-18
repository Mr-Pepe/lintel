pydoclint - docstring style checker
====================================

[![Type checks: mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=555555)](https://pycqa.github.io/isort/)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


.. image:: https://github.com/PyCQA/pydoclint/workflows/Run%20tests/badge.svg
    :target: https://github.com/PyCQA/pydoclint/actions?query=workflow%3A%22Run+tests%22+branch%3Amaster

.. image:: https://readthedocs.org/projects/pydoclint/badge/?version=latest
    :target: https://readthedocs.org/projects/pydoclint/?badge=latest
    :alt: Documentation Status

.. image:: https://pepy.tech/badge/pydoclint
    :target: https://pepy.tech/project/pydoclint

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/


**pydoclint** is a static analysis tool for checking compliance with Python
docstring conventions.

It started as a fork of `pydocstyle <https://github.com/PyCQA/pydocstyle>` with the goal to
eventually also cover the functionality provided by `pylint's <https://github.com/PyCQA/pylint>`
`docparams extension <https://pylint.pycqa.org/en/latest/user_guide/checkers/extensions.html#pylint-extensions-docparams>`.

Read the docs at ...

Todos:

- TODO: Add check for descriptive mood

- Try out pre-commit

- Rename pep257 to default

- Create error table
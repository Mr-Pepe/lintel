Lintel's documentation
==========================

**Lintel** is a static analysis tool for checking compliance with Python
docstring conventions.

.. toctree::
   :maxdepth: 2

   usage
   error_codes
   license


Credits
=======

Lintel started as a fork of `pydocstyle <https://github.com/PyCQA/pydocstyle>`_ with the goal to
eventually also cover the functionality provided by `pylint's <https://github.com/PyCQA/pylint>`_
`docparams extension <https://pylint.pycqa.org/en/latest/user_guide/checkers/extensions.html#pylint-extensions-docparams>`_.

Lintel behaves very similar to pydocstyle in terms of docstring checks but it lacks some
of the more advanced configuration options, e.g., configuration inheritance.

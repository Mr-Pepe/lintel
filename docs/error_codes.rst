Error Codes
===========

Grouping
--------

.. include:: snippets/error_code_table.rst

Conventions
-----------

Not all error codes are checked for by default. There are three conventions
that may be used by pydoclint: ``pep257``, ``numpy`` and ``google``.

The ``pep257`` convention supports `PEP257
<http://www.python.org/dev/peps/pep-0257/>`_) and is used by default.

The ``numpy`` convention supports the `numpydoc docstring
<https://github.com/numpy/numpydoc>`_ standard.

The ``google`` convention supports the `Google Python Style
Guide <https://google.github.io/styleguide/pyguide.html>`_.

These conventions may be specified using ``--convention=<name>`` when
running pydoclint from the command line or by specifying the
convention in a configuration file.

Two more conventions can be used: ``all`` and ``none``.
They check for all or no errors and can be used to quickly create a custom convention by
adding or ignoring specific checks.


Publicity
---------

.. include:: snippets/publicity.rst

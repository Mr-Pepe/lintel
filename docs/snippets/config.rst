``pydoclint`` supports *ini*-like and *toml* configuration files.
In order for ``pydoclint`` to use a configuration file automatically, it must
be named one of the following options.

* ``setup.cfg``
* ``tox.ini``
* ``pyproject.toml``

When searching for a configuration file, ``pydoclint`` looks for one of the
file specified above *in that exact order* in the current working directory.
A configuration file can also be provided via the ``--config`` CLI option.
*ini*-like configuration files must have a ``[pydoclint]`` section while *toml*
configuration files must have a ``[tool.pydoclint]`` section.


Available Options
#################

Get available configuration options by running::

    pydoclint --help


Example
#######

.. code::

    [pydoclint]
    ignore = D100,D203,D405


``lintel`` supports *ini*-like and *toml* configuration files.
In order for ``lintel`` to use a configuration file automatically, it must
be named one of the following options.

* ``setup.cfg``
* ``tox.ini``
* ``pyproject.toml``

When searching for a configuration file, ``lintel`` looks for one of the
file specified above *in that exact order* in the current working directory.
A configuration file can also be provided via the ``--config`` CLI option.
*ini*-like configuration files must have a ``[lintel]`` section while *toml*
configuration files must have a ``[tool.lintel]`` section.


Available Options
#################

Get available configuration options by running::

    lintel --help


Example
#######

.. code::

    [lintel]
    ignore = D100,D203,D405


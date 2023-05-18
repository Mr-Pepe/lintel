**lintel** can be included as a hook for `pre-commit`_.  The easiest way to get
started is to add this configuration to your ``.pre-commit-config.yaml``:

.. parsed-literal::

    -   repo: https://github.com/Mr-Pepe/lintel
        rev: \ |version| \  # pick a git hash / tag to point to
        hooks:
        -   id: lintel

See the `pre-commit docs`_ for how to customize this configuration.

.. _pre-commit:
    https://pre-commit.com/
.. _pre-commit docs:
    https://pre-commit.com/#pre-commit-configyaml---hooks

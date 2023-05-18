``lintel`` supports module-level or inline commenting to skip specific checks on
specific modules, classes, or functions/methods. The supported comments that can be added are:

1. ``# lintel: noqa`` on the module level deactivates lintel for a module.

2. ``# noqa: D100`` on the module level deactivates the D100 check for a module.

3. ``# noqa`` inline skips all checks for the function or class on that line.

4. ``# noqa: D102,D203`` inline can be used to skip specific checks for a specific class or function.

For example, this will skip the check for a period at the end of a function
docstring::

    >>> def bad_function():  # noqa: D400
    ...     """Omit a period in the docstring as an exception"""
    ...     pass

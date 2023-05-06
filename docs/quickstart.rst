Quick Start
===========

1. Install

    .. code::

        pip install pydoclint

2. Run

    .. code::

        $ pydoclint test.py
        test.py:18 in private nested class `meta`:
                D101: Docstring missing
        test.py:27 in public function `get_user`:
            D300: Use """triple double quotes""" (found '''-quotes).
        test:75 in public function `init_database`:
            D201: No blank lines allowed before function docstring (found 1).
        ...

3. Fix your code :)


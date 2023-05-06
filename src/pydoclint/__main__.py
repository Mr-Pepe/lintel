#! /usr/bin/env python
"""Static analysis tool for checking docstring conventions and style."""


if __name__ == '__main__':
    from pydoclint import cli

    cli.app()

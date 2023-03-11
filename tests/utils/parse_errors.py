"""Contains utility functions for tests."""


import os
from typing import Dict


def parse_errors(error: str) -> Dict[str, set]:
    """Parse `error` to a dictionary of {filename: error_codes}.

    This is for test purposes only. All file names should be different.
    """
    result: Dict[str, set] = {}
    py_ext = '.py'
    lines = error.split('\n')
    while lines:
        curr_line = lines.pop(0)
        filename = curr_line[: curr_line.find(py_ext) + len(py_ext)]
        if lines:
            err_line = lines.pop(0).strip()
            err_code = err_line.split(':')[0]
            basename = os.path.basename(filename)
            result.setdefault(basename, set()).add(err_code)

    return result

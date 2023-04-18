"""Old parser tests."""

import re
from pathlib import Path

import pytest

from pydocstyle import Configuration, DocstringError, check_source, get_error_codes


@pytest.mark.parametrize(
    'test_case',
    [
        'test',
        'unicode_literals',
        'nested_class',
        'capitalization',
        'comment_after_def_bug',
        'multi_line_summary_start',
        'all_import',
        'all_import_as',
        'superfluous_quotes',
        'noqa',
        'sections',
        'functions',
        'canonical_google_examples',
        'canonical_numpy_examples',
        'canonical_pep257_examples',
    ],
)
def test_complex_file(test_case: str, resource_dir: Path) -> None:
    """Run domain-specific tests from test.py file."""
    case_module = __import__(
        f'resources.{test_case}',
        globals=globals(),
        locals=locals(),
        fromlist=['expectation'],
        level=2,
    )
    test_case_file = resource_dir / f"{test_case}.py"

    config = Configuration(
        select=set(get_error_codes()),
        ignore_decorators=re.compile('wraps|ignored_decorator'),
    )
    results = list(check_source(test_case_file, config))
    for error in results:
        assert isinstance(error, DocstringError)

    assert case_module.expectation.expected == {(e.node_name, e.message) for e in results}

"""Old parser tests."""

from pathlib import Path

import pytest

from lintel import Configuration, Convention, DocstringError, check_source


@pytest.mark.parametrize(
    ('test_case', "convention"),
    [
        ('test', Convention.ALL),
        ('unicode_literals', Convention.ALL),
        ('nested_class', Convention.ALL),
        ('capitalization', Convention.ALL),
        ('comment_after_def_bug', Convention.ALL),
        ('multi_line_summary_start', Convention.ALL),
        ('all_import', Convention.ALL),
        ('all_import_as', Convention.ALL),
        ('superfluous_quotes', Convention.ALL),
        ('noqa', Convention.ALL),
        ('numpy_sections', Convention.NUMPY),
        ('google_sections', Convention.GOOGLE),
        ('functions', Convention.DEFAULT),
        ('canonical_google_examples', Convention.GOOGLE),
        ('canonical_numpy_examples', Convention.NUMPY),
        ('canonical_pep257_examples', Convention.DEFAULT),
    ],
)
def test_complex_file(test_case: str, convention: Convention, resource_dir: Path) -> None:
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
        convention=convention,
        ignore_decorators='wraps|ignored_decorator',
    )
    results = check_source(test_case_file, config)
    for error in results:
        assert isinstance(error, DocstringError)

    assert {(e.node_name, e.message) for e in results} == case_module.expectation.expected

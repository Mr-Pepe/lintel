"""Contains pytest fixtures."""

from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).parent


@pytest.fixture(scope="session", name="resource_dir")
def resource_dir_fixture() -> Path:
    """Return the path to the test resource directory."""
    return TESTS_DIR / "resources"

"""Contains pytest fixtures."""

from pathlib import Path

import pytest
from tests.utils.sandbox_env import SandboxEnv

TESTS_DIR = Path(__file__).parent


@pytest.fixture(scope="session", name="resource_dir")
def resource_dir_fixture() -> Path:
    """Return the path to the test resource directory."""
    return TESTS_DIR / "resources"


@pytest.fixture(scope="session", name="discovery_dir")
def file_discovery_dir_fixture(resource_dir: Path) -> Path:
    """Return the path to the test resource directory for file discovery."""
    return resource_dir / "file_discovery"


@pytest.fixture(scope="function", params=['ini', 'toml'])
def env(request):
    """Add a testing environment to a test method."""
    sandbox_settings = {
        'ini': {
            'section_name': 'lintel',
            'config_name': 'tox.ini',
        },
        'toml': {
            'section_name': 'tool.lintel',
            'config_name': 'pyproject.toml',
        },
    }[request.param]
    with SandboxEnv(**sandbox_settings) as test_env:
        yield test_env

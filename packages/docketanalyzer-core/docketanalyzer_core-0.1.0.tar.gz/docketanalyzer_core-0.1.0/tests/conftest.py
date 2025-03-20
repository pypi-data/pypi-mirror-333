import pytest
from pathlib import Path


@pytest.fixture
def fixture_path():
    """Path to the fixtures directory."""
    return Path(__file__).parent / "fixtures"

import pytest


@pytest.fixture
def database_path(tmp_path):
    return tmp_path / "test.db"
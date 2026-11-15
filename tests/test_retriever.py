
import pytest

from database.connection import get_connection
from database.schema import create_machines_table, create_writeups_table
from database.writeups import add_writeup
from knowledge_base.retriever import get_machine_knowledge


@pytest.fixture
def test_db(tmp_path):
    """Create a temporary database for testing."""

    db_path = tmp_path / "test.db"

    create_machines_table(db_path)
    create_writeups_table(db_path)

    with get_connection(db_path) as connection:
        connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Blue', 'Windows', 'Easy')
        """)

    return db_path


def test_get_machine_knowledge(test_db):
    """Test retrieving a machine and its writeups."""

    add_writeup(
        machine_id=1,
        title="Blue Official Walkthrough",
        content="# Blue\n\nA Windows SMB exploitation walkthrough.",
        db_path=test_db
    )

    result = get_machine_knowledge(1, db_path=test_db)

    assert result is not None
    assert result["machine"]["name"] == "Blue"
    assert result["machine"]["os"] == "Windows"
    assert len(result["writeups"]) == 1
    assert result["writeups"][0]["title"] == "Blue Official Walkthrough"


def test_get_machine_knowledge_no_writeups(test_db):
    """Test retrieving a machine with no writeups."""

    result = get_machine_knowledge(1, db_path=test_db)

    assert result is not None
    assert result["machine"]["name"] == "Blue"
    assert result["writeups"] == []


def test_get_machine_knowledge_nonexistent_machine(test_db):
    """Test retrieving a machine that doesn't exist."""

    result = get_machine_knowledge(999, db_path=test_db)

    assert result is None

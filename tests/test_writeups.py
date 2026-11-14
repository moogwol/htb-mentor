
from dataclasses import fields

import pytest
import sqlite3

from database.connection import get_connection
from database.schema import create_machines_table, create_writeups_table
from database.writeups import add_writeup, get_writeup, get_writeups_by_machine, update_writeup, delete_writeup


@pytest.fixture
def test_db(tmp_path):
    """Create a temporary database for testing."""

    db_path = tmp_path / "test.db"

    create_machines_table(db_path)
    create_writeups_table(db_path)

    # Insert a machine for the writeup to reference
    with get_connection(db_path) as connection:
        connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Devel', 'Windows', 'Easy')
        """)

    return db_path


def test_add_writeup(test_db):
    """Test that a writeup can be successfully added."""

    writeup_id = add_writeup(
        machine_id=1,
        title="Devel Official Walkthrough",
        content="# Devel\n\nAn IIS exploitation walkthrough.",
        source="https://example.com/devel",
        db_path=test_db
    )

    assert writeup_id == 1

    with get_connection(test_db) as connection:
        result = connection.execute(
            "SELECT * FROM writeups WHERE id = ?",
            (writeup_id,)
        ).fetchone()

    assert result is not None
    assert result["machine_id"] == 1
    assert result["title"] == "Devel Official Walkthrough"
    assert result["content"] == "# Devel\n\nAn IIS exploitation walkthrough."
    assert result["source"] == "https://example.com/devel"


def test_add_writeup_invalid_machine(test_db):
    """Test that a writeup cannot reference a nonexistent machine."""

    with pytest.raises(sqlite3.IntegrityError):
        add_writeup(
            machine_id=999,
            title="Invalid Walkthrough",
            content="Some content",
            db_path=test_db
        )


def test_get_writeup(test_db):
    """Test retrieving an existing walkthrough."""

    writeup_id = add_writeup(
        machine_id=1,
        title="Devel Walkthrough",
        content="Test content",
        db_path=test_db
    )

    result = get_writeup(writeup_id, db_path=test_db)

    assert result is not None
    assert result["title"] == "Devel Walkthrough"
    assert result["content"] == "Test content"


def test_get_nonexistent_writeup(test_db):
    """Test retrieving a walkthrough that doesn't exist."""

    result = get_writeup(999, db_path=test_db)

    assert result is None



def test_get_writeups_for_machine(test_db):
    """Test retrieving all walkthroughs for a machine."""

    add_writeup(1, "Official Walkthrough", "Official content",
                db_path=test_db)

    add_writeup(1, "Community Walkthrough", "Community content",
                db_path=test_db)

    results = get_writeups_by_machine(1, db_path=test_db)

    assert len(results) == 2
    assert {result["title"] for result in results} == {
        "Official Walkthrough",
        "Community Walkthrough"
    }


def test_get_writeups_for_machine_no_results(test_db):
    """Test retrieving walkthroughs for a machine with none."""

    results = get_writeups_by_machine(1, db_path=test_db)

    assert len(results) == 0
    


def test_update_writeup(test_db):
    """Test updating an existing walkthrough."""

    writeup_id = add_writeup(
        1, "Original Title", "Original content",
        db_path=test_db
    )

    result = update_writeup(
        writeup_id,
        "Updated Title",
        "Updated content",
        "https://example.com/updated",
        db_path=test_db
    )

    assert result is True

    writeup = get_writeup(writeup_id, db_path=test_db)

    assert writeup["title"] == "Updated Title"
    assert writeup["content"] == "Updated content"
    assert writeup["source"] == "https://example.com/updated"


def test_update_nonexistent_writeup(test_db):
    """Test updating a walkthrough that doesn't exist."""

    result = update_writeup(
        999, "Title", "Content",
        db_path=test_db
    )

    assert result is False
              
         

def test_delete_writeup(test_db):
    """Test deleting an existing walkthrough."""

    writeup_id = add_writeup(
        1, "Devel Walkthrough", "Some content",
        db_path=test_db
    )

    result = delete_writeup(writeup_id, db_path=test_db)

    assert result is True
    assert get_writeup(writeup_id, db_path=test_db) is None


def test_delete_nonexistent_writeup(test_db):
    """Test deleting a walkthrough that doesn't exist."""

    result = delete_writeup(999, db_path=test_db)

    assert result is False

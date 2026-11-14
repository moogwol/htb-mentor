
import pytest
import sqlite3

from database.connection import get_connection
from database.schema import create_machines_table, create_writeups_table
from database.writeups import get_writeup
from knowledge_base.importer import import_writeup


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test.db"

    create_machines_table(db_path)
    create_writeups_table(db_path)

    with get_connection(db_path) as connection:
        connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Devel', 'Windows', 'Easy')
        """)

    return db_path


def test_import_writeup(test_db, tmp_path):
    """Test importing a Markdown walkthrough."""

    file_path = tmp_path / "devel.md"

    content = """# Devel

## Enumeration

Port 80 is running IIS.

## Exploitation

A vulnerability is exploited.
"""

    file_path.write_text(content, encoding="utf-8")

    writeup_id = import_writeup(
        machine_id=1,
        file_path=file_path,
        title="Devel Official Walkthrough",
        source="https://example.com/devel",
        db_path=test_db
    )

    result = get_writeup(writeup_id, db_path=test_db)

    assert result is not None
    assert result["title"] == "Devel Official Walkthrough"
    assert result["content"] == content
    assert result["source"] == "https://example.com/devel"


def test_import_missing_file(test_db, tmp_path):
    """Test importing a file that doesn't exist."""

    with pytest.raises(FileNotFoundError):
        import_writeup(
            machine_id=1,
            file_path=tmp_path / "missing.md",
            title="Missing",
            db_path=test_db
        )


def test_import_empty_file(test_db, tmp_path):
    """Test importing an empty Markdown file."""

    file_path = tmp_path / "empty.md"
    file_path.write_text("   ", encoding="utf-8")

    with pytest.raises(ValueError):
        import_writeup(
            machine_id=1,
            file_path=file_path,
            title="Empty",
            db_path=test_db
        )


def test_import_invalid_machine(test_db, tmp_path):
    """Test importing against a nonexistent machine."""

    file_path = tmp_path / "devel.md"
    file_path.write_text("# Devel", encoding="utf-8")

    with pytest.raises(sqlite3.IntegrityError):
        import_writeup(
            machine_id=999,
            file_path=file_path,
            title="Devel",
            db_path=test_db
        )

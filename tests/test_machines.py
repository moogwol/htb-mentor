from database.connection import get_connection
from database.schema import create_machines_table
from database.machines import get_all_machines


def test_get_all_machines(tmp_path):
    """Test retrieving all machines."""

    db_path = tmp_path / "test.db"
    create_machines_table(db_path)

    with get_connection(db_path) as connection:
        connection.executemany("""
            INSERT INTO machines (name, os, difficulty)
            VALUES (?, ?, ?)
        """, [
            ("Devel", "Windows", "Easy"),
            ("Lame", "Linux", "Easy"),
            ("Blue", "Windows", "Medium")
        ])

    results = get_all_machines(db_path)

    assert len(results) == 3
    assert results[0]["name"] == "Blue"
    assert results[1]["name"] == "Devel"
    assert results[2]["name"] == "Lame"


def test_get_all_machines_empty_database(tmp_path):
    """Test retrieving machines when none exist."""

    db_path = tmp_path / "test.db"
    create_machines_table(db_path)

    results = get_all_machines(db_path)

    assert results == []
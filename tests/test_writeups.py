import sqlite3
import pytest

from database.schema import (
    create_machines_table,
    create_writeups_table
)
from database.connection import get_connection


def test_create_writeups_table(database_path):
    create_machines_table(database_path)
    create_writeups_table(database_path)

    with get_connection(database_path) as connection:
        result = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'writeups'
        """).fetchone()

    assert result is not None
    assert result["name"] == "writeups"


def test_writeup_requires_existing_machine(database_path):
    create_machines_table(database_path)
    create_writeups_table(database_path)

    with pytest.raises(sqlite3.IntegrityError):
        with get_connection(database_path) as connection:
            connection.execute("""
                INSERT INTO writeups (machine_id, title, content)
                VALUES (999, 'Test writeup', 'Test content')
            """)
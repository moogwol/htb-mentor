from database.schema import (
    create_machines_table,
    create_conversations_table
)
from database.connection import get_connection


def test_create_conversations_table(database_path):
    create_machines_table(database_path)
    create_conversations_table(database_path)

    with get_connection(database_path) as connection:
        result = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'conversations'
        """).fetchone()

    assert result is not None
    assert result["name"] == "conversations"


def test_conversation_requires_existing_machine(database_path):
    create_machines_table(database_path)
    create_conversations_table(database_path)

    import sqlite3
    import pytest

    with pytest.raises(sqlite3.IntegrityError):
        with get_connection(database_path) as connection:
            connection.execute("""
                INSERT INTO conversations (machine_id, title)
                VALUES (999, 'Test conversation')
            """)
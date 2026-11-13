import pytest
import sqlite3

from database.schema import (
    create_machines_table,
    create_conversations_table,
    create_messages_table
)
from database.connection import get_connection


def test_create_messages_table(database_path):
    create_machines_table(database_path)
    create_conversations_table(database_path)
    create_messages_table(database_path)

    with get_connection(database_path) as connection:
        result = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'messages'
        """).fetchone()

    assert result is not None
    assert result["name"] == "messages"


def test_insert_message(database_path):
    create_machines_table(database_path)
    create_conversations_table(database_path)
    create_messages_table(database_path)

    with get_connection(database_path) as connection:
        machine = connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Devel', 'Windows', 'Easy')
        """)

        machine_id = machine.lastrowid

        conversation = connection.execute("""
            INSERT INTO conversations (machine_id, title)
            VALUES (?, ?)
        """, (machine_id, 'Initial enumeration'))

        conversation_id = conversation.lastrowid

        connection.execute("""
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
        """, (conversation_id, 'user', 'What should I enumerate first?'))

        result = connection.execute("""
            SELECT role, content
            FROM messages
            WHERE conversation_id = ?
        """, (conversation_id,)).fetchone()

    assert result["role"] == "user"
    assert result["content"] == "What should I enumerate first?"


def test_invalid_message_role(database_path):
    create_machines_table(database_path)
    create_conversations_table(database_path)
    create_messages_table(database_path)

    with get_connection(database_path) as connection:
        machine = connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Devel', 'Windows', 'Easy')
        """)

        conversation = connection.execute("""
            INSERT INTO conversations (machine_id, title)
            VALUES (?, ?)
        """, (machine.lastrowid, 'Test'))

        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("""
                INSERT INTO messages (conversation_id, role, content)
                VALUES (?, ?, ?)
            """, (conversation.lastrowid, 'hacker', 'Invalid role'))
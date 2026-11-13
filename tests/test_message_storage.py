from database.schema import (
    create_machines_table,
    create_conversations_table,
    create_messages_table
)
from database.connection import get_connection
from database.conversations import create_conversation
from database.messages import add_message, get_messages


def test_save_and_retrieve_messages(database_path):
    create_machines_table(database_path)
    create_conversations_table(database_path)
    create_messages_table(database_path)

    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Devel', 'Windows', 'Easy')
            """
        )
        machine_id = cursor.lastrowid

    conversation_id = create_conversation(
        machine_id,
        "Initial enumeration",
        database_path
    )

    add_message(
        conversation_id,
        "user",
        "What should I enumerate first?",
        database_path
    )

    add_message(
        conversation_id,
        "assistant",
        "Start with an Nmap scan.",
        database_path
    )

    messages = get_messages(conversation_id, database_path)

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "Start with an Nmap scan."
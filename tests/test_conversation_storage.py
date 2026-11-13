from database.connection import get_connection
from database.schema import (
    create_machines_table,
    create_conversations_table
)
from database.conversations import (
    create_conversation,
    get_conversation
)


def test_create_and_retrieve_conversation(database_path):
    create_machines_table(database_path)
    create_conversations_table(database_path)

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

    result = get_conversation(conversation_id, database_path)

    assert result["title"] == "Initial enumeration"
    assert result["machine_id"] == machine_id
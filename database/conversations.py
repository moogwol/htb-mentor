from database.connection import get_connection


def create_conversation(machine_id, title, db_path=None):
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO conversations (machine_id, title)
            VALUES (?, ?)
            """,
            (machine_id, title)
        )

        return cursor.lastrowid


def get_conversation(conversation_id, db_path=None):
    with get_connection(db_path) as connection:
        result = connection.execute(
            """
            SELECT *
            FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        ).fetchone()

        return dict(result) if result else None
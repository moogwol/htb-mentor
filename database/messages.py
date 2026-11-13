from database.connection import get_connection


def add_message(conversation_id, role, content, db_path=None):
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content)
        )

        connection.execute(
            """
            UPDATE conversations
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (conversation_id,)
        )

        return cursor.lastrowid


def get_messages(conversation_id, db_path=None):
    with get_connection(db_path) as connection:
        results = connection.execute(
            """
            SELECT id, role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,)
        ).fetchall()

        return [dict(row) for row in results]
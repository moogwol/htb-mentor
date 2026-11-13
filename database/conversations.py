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
    
def get_all_conversations(db_path=None):
    with get_connection(db_path) as connection:
        results = connection.execute(
            """
            SELECT id, machine_id, title, created_at
            FROM conversations
            ORDER BY id DESC
            """
        ).fetchall()

        return [dict(row) for row in results]    
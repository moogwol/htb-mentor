import sqlite3

DB_NAME = "htb_mentor.db"


def initialize_database():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_message(role, content):

    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO messages (role, content)
        VALUES (?, ?)
        """,
        (role, content)
    )

    conn.commit()
    conn.close()


def load_history():

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        """
        SELECT role, content
        FROM messages
        ORDER BY timestamp ASC
        """
    ).fetchall()

    conn.close()

    return [
        {
            "role": role,
            "content": content
        }
        for role, content in rows
    ]
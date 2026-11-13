from database.connection import DATABASE_PATH, get_connection

def create_machines_table(db_path=None):
    """""Create the 'machines' table in the database if it doesn't already exist."""

    with get_connection(db_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS machines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                os TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'not started',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                CHECK (os IN ('Windows', 'Linux')),
                CHECK (difficulty IN ('Easy', 'Medium', 'Hard', 'Insane')),
                CHECK (status IN ('not started', 'Active', 'Completed'))
            )
        """)
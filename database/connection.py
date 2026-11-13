
import sqlite3
from pathlib import Path
from contextlib import contextmanager


# Locate the project root relative to this file
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "data" / "mentor.db"


@contextmanager
def get_connection():
    """Create and manage a SQLite database connection."""

    # Ensure the database directory exists
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    # Return database rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    # Enable foreign key enforcement
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        with connection:
            yield connection
    finally:
        connection.close()

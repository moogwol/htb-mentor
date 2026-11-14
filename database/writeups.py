from database.connection import get_connection

def add_writeup(machine_id, title, content, source=None, db_path=None):
    """Add a new writeup to the database."""
    
    with get_connection(db_path) as connection:
        cursor = connection.execute("""
            INSERT INTO writeups (machine_id, title, content, source)
            VALUES (?, ?, ?, ?)
        """, (machine_id, title, content, source))
        return cursor.lastrowid


def get_writeup(writeup_id, db_path=None):
    """Retrieve a writeup from the database by its ID."""
    
    with get_connection(db_path) as connection:
         result = connection.execute("""
            SELECT *
            FROM writeups
            WHERE id = ?
        """, (writeup_id,)).fetchone()
         
    return result


def get_writeups_by_machine(machine_id, db_path=None):
    """Retrieve all writeups for a specific machine."""
    
    with get_connection(db_path) as connection:
        results = connection.execute("""
            SELECT *
            FROM writeups
            WHERE machine_id = ?
            ORDER BY created_at DESC
        """, (machine_id,)).fetchall()
        
    return results

def update_writeup(writeup_id, title=None, content=None, source=None, db_path=None):
    """Update an existing writeup in the database."""
    
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            UPDATE writeups
            SET title = ?, content = ?, source = ?
            WHERE id = ?
            """, (title, content, source, writeup_id))
                        
        return cursor.rowcount > 0  # Returns the number of rows updated
    

def delete_writeup(writeup_id, db_path=None):
    """Delete a walkthrough by its ID."""

    with get_connection(db_path) as connection:
        cursor = connection.execute("""
            DELETE FROM writeups
            WHERE id = ?
        """, (writeup_id,))

        return cursor.rowcount > 0
    
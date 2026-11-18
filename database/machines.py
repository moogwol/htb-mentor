from database.connection import get_connection


def create_machine(name, os, difficulty, machine_info=None, db_path=None):
    """Create a new machine in the database."""

    with get_connection(db_path) as connection:
        cursor =connection.execute(
            """
            INSERT INTO machines (name, os, difficulty, machine_info)
            VALUES (?, ?, ?, ?)
            """,
            (name, os, difficulty, machine_info))  
        
        return cursor.lastrowid  # Return the ID of the newly created machine
        


def get_all_machines(db_path=None):
    """Retrieve all machines from the database."""

    with get_connection(db_path) as connection:
        results = connection.execute("""
                                    SELECT *
                                    FROM machines
                                    ORDER BY name
                                    """).fetchall()
        
        return [dict(row) for row in results]

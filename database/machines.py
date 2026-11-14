from database.connection import get_connection


def get_all_machines(db_path=None):
    """Retrieve all machines from the database."""

    with get_connection(db_path) as connection:
        results = connection.execute("""
                                    SELECT *
                                    FROM machines
                                    ORDER BY name
                                    """).fetchall()
        return results

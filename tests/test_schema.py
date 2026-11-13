from database.schema import create_machines_table
from database.connection import get_connection


def test_create_machines_table(database_path):
    # Arrange: create the table in a temporary database
    create_machines_table(database_path)

    # Act: check whether the table exists
    with get_connection(database_path) as connection:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'machines'
            """
        ).fetchone()

    # Assert
    assert result is not None
    assert result["name"] == "machines"
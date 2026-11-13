from database.connection import get_connection


def test_connection():
    with get_connection() as connection:

        result = connection.execute(
            "SELECT sqlite_version()"
        )

        version = result.fetchone()[0]

        print(f"SQLite version: {version}")

        foreign_keys = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()[0]

        print(f"Foreign keys enabled: {foreign_keys}")


if __name__ == "__main__":
    test_connection()
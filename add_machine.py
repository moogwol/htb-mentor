from database.connection import get_connection

with get_connection() as connection:
    connection.execute(
        """
        INSERT INTO machines (name, os, difficulty)
        VALUES (?, ?, ?)
        """,
        ("Devel", "Windows", "Easy")
    )

print("Devel added successfully.")
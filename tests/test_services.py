import sqlite3
import pytest

from database.schema import create_services_table, create_machines_table
from database.connection import get_connection
from database.services import (add_service,
                               get_services_by_machine,
                               get_service,
                               update_service,
                               delete_service)


def test_create_services_table(database_path):
    create_services_table(database_path)

    with get_connection(database_path) as connection:
        result = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'services'
        """).fetchone()

    assert result is not None
    assert result["name"] == "services"
    
    
def test_service_requires_valid_machine(database_path):
    create_machines_table(database_path)
    create_services_table(database_path)

    with get_connection(database_path) as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("""
                INSERT INTO services (
                    machine_id, port, protocol, name
                )
                VALUES (999, 80, 'TCP', 'HTTP')
            """)    


def test_service_port_protocol_must_be_unique_per_machine(database_path):
    create_machines_table(database_path)
    create_services_table(database_path)

    with get_connection(database_path) as connection:
        cursor = connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Lame', 'Linux', 'Easy')
        """)

        machine_id = cursor.lastrowid

        connection.execute("""
            INSERT INTO services (machine_id, port, protocol, name)
            VALUES (?, 22, 'TCP', 'SSH')
        """, (machine_id,))

        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("""
                INSERT INTO services (machine_id, port, protocol, name)
                VALUES (?, 22, 'TCP', 'SSH')
            """, (machine_id,))
        

def test_add_service(database_path):
    create_machines_table(database_path)
    create_services_table(database_path)

    with get_connection(database_path) as connection:
        cursor = connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Lame', 'Linux', 'Easy')
        """)
        machine_id = cursor.lastrowid

    # First connection has now closed
    service_id = add_service(
        machine_id, 22, "TCP", "SSH",
        db_path=database_path
    )

    with get_connection(database_path) as connection:
        result = connection.execute(
            "SELECT * FROM services WHERE id = ?",
            (service_id,)
        ).fetchone()

    assert service_id is not None
    assert result["port"] == 22
    assert result["name"] == "SSH"        
    
def test_get_services_by_machine(database_path):
    create_machines_table(database_path)
    create_services_table(database_path)

    # Create a machine
    with get_connection(database_path) as connection:
        cursor = connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Lame', 'Linux', 'Easy')
        """)
        machine_id = cursor.lastrowid

    # Add two services
    add_service(machine_id, 80, "TCP", "HTTP", db_path=database_path)
    add_service(machine_id, 22, "TCP", "SSH", db_path=database_path)

    # Retrieve services
    services = get_services_by_machine(machine_id, db_path=database_path)

    # Check results
    assert len(services) == 2
    assert services[0]["port"] == 22
    assert services[1]["port"] == 80
    
    
def test_get_service(database_path):
    create_machines_table(database_path)
    create_services_table(database_path)

    # Create a machine
    with get_connection(database_path) as connection:
        cursor = connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Lame', 'Linux', 'Easy')
        """)
        machine_id = cursor.lastrowid

    # Add a service
    service_id = add_service(
        machine_id, 22, "TCP", "SSH",
        version="OpenSSH 8.2",
        db_path=database_path
    )

    # Retrieve the service
    service = get_service(service_id, db_path=database_path)

    # Check the result
    assert service is not None
    assert service["id"] == service_id
    assert service["name"] == "SSH"
    assert service["version"] == "OpenSSH 8.2" 
    
    
def test_update_service(database_path):
    create_machines_table(database_path)
    create_services_table(database_path)

    # Create a machine
    with get_connection(database_path) as connection:
        cursor = connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Lame', 'Linux', 'Easy')
        """)
        machine_id = cursor.lastrowid

    # Add a service
    service_id = add_service(
        machine_id, 22, "TCP", "SSH",
        version="OpenSSH 8.2",
        notes="Initial discovery",
        db_path=database_path
    )

    # Update only the version
    result = update_service(
        service_id,
        version="OpenSSH 9.2",
        db_path=database_path
    )

    # Retrieve the updated service
    service = get_service(service_id, db_path=database_path)

    # Check the update
    assert result is True
    assert service["version"] == "OpenSSH 9.2"
    assert service["name"] == "SSH"
    assert service["notes"] == "Initial discovery"      
    
def test_delete_service(database_path):
    create_machines_table(database_path)
    create_services_table(database_path)

    # Create a machine
    with get_connection(database_path) as connection:
        cursor = connection.execute("""
            INSERT INTO machines (name, os, difficulty)
            VALUES ('Lame', 'Linux', 'Easy')
        """)
        machine_id = cursor.lastrowid

    # Add a service
    service_id = add_service(
        machine_id, 22, "TCP", "SSH",
        db_path=database_path
    )

    # Delete the service
    result = delete_service(
        service_id, db_path=database_path
    )

    # Verify deletion
    service = get_service(
        service_id, db_path=database_path
    )

    assert result is True
    assert service is None         
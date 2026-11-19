from database.connection import get_connection

def add_service(machine_id,
                port,
                protocol,
                name,
                version=None,
                state="open",
                notes=None,
                db_path=None
                ):
    """Add a service to the database"""
    
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO services (
                machine_id, port, protocol, name, version, state, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                machine_id, port, protocol, name, version, state, notes
            )
        )
        
        return cursor.lastrowid
    
    
def get_services_by_machine(machine_id, db_path=None):
    """Get all service running on a given machine"""
      
        
    with get_connection(db_path) as connection:
         services = connection.execute(
            """
            SELECT * FROM services
            WHERE machine_id = ?
            ORDER BY port ASC
            """,
            (machine_id,)
            ).fetchall()
         
    
    return services


def get_service(service_id, db_path=None):
    """retrieve a service from the database by its id"""
    
    with get_connection(db_path) as connection:
        result = connection.execute(
            """
            SELECT *
            FROM services
            WHERE id = ?
            """, (service_id,)).fetchone()
    
    return result    

def update_service(service_id,
                    name=None,
                    version=None,
                    state=None,
                    notes=None,
                    db_path=None):
    """Update an existing service in the database"""
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """ 
            UPDATE services
            SET name = COALESCE(?, name),
                version = COALESCE(?, version),
                state = COALESCE(?, state),
                notes = COALESCE(?, notes)
            WHERE id = ?  
            """, (name, version, state, notes, service_id))
        
    return cursor.rowcount > 0 # Returns the number of rows updated

def delete_service(service_id, db_path=None):
    """Delete a service by its ID"""
    
    with get_connection(db_path) as connection:
            cursor = connection.execute(
                """
                DELETE FROM services
                WHERE id = ?
                """, (service_id,))
            
            return cursor.rowcount > 0
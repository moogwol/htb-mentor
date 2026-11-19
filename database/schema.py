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
                machine_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                CHECK (os IN ('Windows', 'Linux')),
                CHECK (difficulty IN ('Very Easy', 'Easy', 'Medium', 'Hard', 'Insane')),
                CHECK (status IN ('not started', 'Active', 'Completed'))
            )
        """)
        
def create_writeups_table(db_path=None):
    with get_connection(db_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS writeups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                machine_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (machine_id) REFERENCES machines(id)
            )
        """)       
        
def create_conversations_table(db_path=None):
    with get_connection(db_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                machine_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (machine_id) REFERENCES machines(id)
            )
        """)  
        
def create_messages_table(db_path=None):
    with get_connection(db_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE,

                CHECK (role IN ('user', 'assistant', 'system'))
            )
        """)     
        

def create_services_table(db_path=None):
    with get_connection(db_path) as connection:
        connection.execute("""
                           CREATE TABLE IF NOT EXISTS services (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 machine_id INTEGER NOT NULL,
                                 port INTEGER NOT NULL,
                                 protocol TEXT NOT NULL,
                                 name TEXT NOT NULL,
                                 version TEXT,
                                 state TEXT NOT NULL DEFAULT 'open',
                                 notes TEXT,
                                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                 
                                 FOREIGN KEY (machine_id) REFERENCES machines(id),
                                 
                                 UNIQUE (machine_id, port, protocol)
                           ) 
                           """)

        
def create_all_tables(db_path=None):
    create_machines_table(db_path)
    create_writeups_table(db_path)
    create_conversations_table(db_path)
    create_messages_table(db_path)   
    create_services_table(db_path)               
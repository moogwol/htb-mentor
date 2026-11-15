from database.machines import get_all_machines
from database.writeups import get_writeups_by_machine

def get_machine_knowledge(machine_id, db_path=None):
    """Retrieve knowledge for a specific machine."""
    
    machines = get_all_machines(db_path)
    
    machine = next(
        (m for m in machines if m["id"] == machine_id), 
        None
        )
    
    if machine is None:
        return None

    writeups = get_writeups_by_machine(machine_id, db_path)

    knowledge = {
        "machine": machine,
        "writeups": writeups
    }

    return knowledge
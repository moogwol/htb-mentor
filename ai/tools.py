import json

from database.services import (
    add_service,
    get_services_by_machine,
    get_service,
    update_service,
    delete_service,
)

tools = [
    {
        "type": "function",
        "name": "add_service",
        "description": (
            "Record a newly discovered network service "
            "for a machine in the database."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "machine_id": {
                    "type": "integer",
                    "description": "ID of the machine the service belongs to.",
                },
                "port": {
                    "type": "integer",
                    "description": "Port number, for example 22 or 80.",
                },
                "protocol": {
                    "type": "string",
                    "enum": ["TCP", "UDP"],
                    "description": "Network protocol.",
                },
                "name": {
                    "type": "string",
                    "description": "Service name, for example SSH or HTTP.",
                },
                "version": {
                    "type": ["string", "null"],
                    "description": "Detected service version, if known.",
                },
                "state": {
                    "type": "string",
                    "description": "Service state, normally open, filtered or closed.",
                },
                "notes": {
                    "type": ["string", "null"],
                    "description": "Additional observations about the service.",
                },
            },
            "required": [
                "machine_id",
                "port",
                "protocol",
                "name",
                "version",
                "state",
                "notes",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_services_by_machine",
        "description": (
            "Retrieve all recorded network services for a machine. "
            "Use this to check which services have already been discovered."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "machine_id": {"type": "integer", "description": "ID of the machine."}
            },
            "required": ["machine_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_service",
        "description": "Retrieve a specific recorded service using its service ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "service_id": {
                    "type": "integer",
                    "description": "ID of the service to retrieve.",
                }
            },
            "required": ["service_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "update_service",
        "description": (
            "Update the details of an existing recorded service. "
            "Only provide fields that need changing."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "service_id": {
                    "type": "integer",
                    "description": "ID of the service to update.",
                },
                "name": {
                    "type": ["string", "null"],
                    "description": "Updated service name, or null to leave unchanged.",
                },
                "version": {
                    "type": ["string", "null"],
                    "description": "Updated service version, or null to leave unchanged.",
                },
                "state": {
                    "type": ["string", "null"],
                    "description": "Updated service state, or null to leave unchanged.",
                },
                "notes": {
                    "type": ["string", "null"],
                    "description": "Updated notes, or null to leave unchanged.",
                },
            },
            "required": ["service_id", "name", "version", "state", "notes"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "delete_service",
        "description": (
            "Delete a recorded service using its service ID. "
            "Only use this when the user explicitly requests deletion."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "service_id": {
                    "type": "integer",
                    "description": "ID of the service to delete.",
                }
            },
            "required": ["service_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

available_functions = {
    "add_service": add_service,
    "get_services_by_machine": get_services_by_machine,
    "get_service": get_service,
    "update_service": update_service,
    "delete_service": delete_service,
}


def call_function(name, arguments):
    function = available_functions.get(name)

    if function is None:
        raise ValueError(f"Unknown function: {name}")

    if isinstance(arguments, str):
        arguments = json.loads(arguments)

    return function(**arguments)

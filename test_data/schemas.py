OBJECT_SCHEMA = {
    "type": "object",
    "required": ["id", "name"],
    "properties": {
        "id":        {"type": "string"},
        "name":      {"type": "string"},
        "data":      {"type": ["object", "null"]},
        "createdAt": {"type": ["string", "integer"]},
        "updatedAt": {"type": ["string", "integer"]},
    }
}

PUT_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "updatedAt"],
    "properties": {
        "id":        {"type": "string"},
        "name":      {"type": "string"},
        "data":      {"type": ["object", "null"]},
        "updatedAt": {"type": ["string", "integer"]}
    }
}

AUTH_OBJECT_SCHEMA = {
    "type": "object",
    "required": ["id", "name"],
    "properties": {
        "id":        {"type": "string"},
        "name":      {"type": "string"},
        "data":      {"type": ["object", "null"]},
        "createdAt": {"type": "string"},
        "updatedAt": {"type": "string"},
    }
}

AUTH_LIST_SCHEMA = {
    "type": "array",
    "items": AUTH_OBJECT_SCHEMA
}

AUTH_DELETE_SCHEMA = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {"type": "string"}
    }
}
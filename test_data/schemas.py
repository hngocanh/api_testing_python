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
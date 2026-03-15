CREATE_DEVICE = {
    "name": "Apple MacBook Pro 16",
    "data": {
        "year": 2023,
        "price": 2499.99,
        "CPU model": "Apple M1 Pro",
        "Hard disk size": "512GB",
    }
}

# --- PUT Payloads ---

PUT_FULL_UPDATE = {
    "name": "Apple MacBook Pro 16 (Updated)",
    "data": {
        "year": 2023,
        "price": 1999.99,
        "CPU model": "Apple M3 Pro",
        "Hard disk size": "1 TB",
        "color": "Space Black"
    }
}

PUT_MINIMAL_UPDATE = {
    "name": "Minimal Device",
    "data": None
}

PUT_SAME_VALUES = {
    "name": "Apple MacBook Pro 16",
    "data": {
        "year": 2023,
        "price": 2499.99,
        "CPU model": "Apple M3 Pro",
        "Hard disk size": "512 GB"
    }
}

PUT_DIFFERENT_DATA_TYPES = {
    "name": "Mixed Types Device",
    "data": {
        "count": 42,            # integer
        "price": 9.99,          # float
        "available": True,      # boolean
        "nickname": None,       # null
        "tags": ["a", "b"]      # array
    }
}

PUT_NAME_ONLY = {
    "name": "Name Only Device"
    # no "data" key at all
}

PUT_MISSING_NAME = {
    "data": {
        "price": 999
    }
    # no "name" key — should fail
}

PUT_EMPTY_PAYLOAD = {}

PUT_WRONG_TYPES = {
    "name": 12345,       # integer instead of string — should fail
    "data": "not-an-object"  # string instead of object — should fail
}


PATCH_DEVICE = {
    "name": "Apple MacBook Pro 16 (Patched)"
}

# ── Authenticated tier payloads ──────────────────────────────

AUTH_CREATE_DEVICE = {
    "name": "Apple MacBook Pro 16",
    "data": {
        "year": 2023,
        "price": 2499.99,
        "CPU model": "Apple M3 Pro",
        "Hard disk size": "512 GB"
    }
}

AUTH_CREATE_SECOND_DEVICE = {
    "name": "Apple iPhone 15 Pro",
    "data": {
        "color": "Natural Titanium",
        "storage": "256 GB",
        "price": 999.99
    }
}

AUTH_PUT_UPDATE = {
    "name": "Apple MacBook Pro 16 (Updated)",
    "data": {
        "year": 2024,
        "price": 1999.99,
        "CPU model": "Apple M4 Pro",
        "Hard disk size": "1 TB",
        "color": "Space Black"
    }
}

AUTH_PATCH_UPDATE = {
    "name": "Apple MacBook Pro 16 (Patched)"
}

AUTH_PUT_NULL_DATA = {
    "name": "Minimal Device",
    "data": None
}

AUTH_PUT_MISSING_NAME = {
    "data": {"price": 999}
}

AUTH_PUT_EMPTY = {}

AUTH_PATCH_EMPTY = {}
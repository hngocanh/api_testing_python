from jsonschema import validate
from test_data.schemas import OBJECT_SCHEMA
from test_data.payloads import CREATE_DEVICE

def test_create_object_status_200(public_api):
    response = public_api.create(CREATE_DEVICE)
    assert response.status_code == 200
    obj = response.json()
    public_api.delete_object(obj["id"])

def test_create_object_matches_schema(public_api):
    response = public_api.create(CREATE_DEVICE)
    obj = response.json()
    validate(instance=obj, schema=OBJECT_SCHEMA)  # fails if shape is wrong
    public_api.delete_object(obj["id"])

def test_create_object_name_matches_payload(public_api):
    response = public_api.create(CREATE_DEVICE)
    obj = response.json()
    assert obj["name"] == CREATE_DEVICE["name"]
    public_api.delete_object(obj["id"])
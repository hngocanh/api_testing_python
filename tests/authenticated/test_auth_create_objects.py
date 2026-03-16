from jsonschema import validate
from test_data.schemas import AUTH_OBJECT_SCHEMA, AUTH_LIST_SCHEMA
from test_data.payloads import AUTH_CREATE_SECOND_DEVICE, AUTH_CREATE_DEVICE, AUTH_PATCH_EMPTY, AUTH_PATCH_UPDATE, AUTH_PUT_EMPTY, AUTH_PUT_UPDATE, AUTH_PUT_MISSING_NAME, AUTH_PUT_NULL_DATA

class TestAuthCreateHappyPath:

    def test_create_object_returns_200(self, auth_api):
        response = auth_api.create(AUTH_CREATE_DEVICE)
        obj = response.json()
        assert response.status_code == 200
        auth_api.delete_object(obj["id"])

    def test_create_object_matches_schema(self, auth_api):
        response = auth_api.create(AUTH_CREATE_DEVICE)
        obj = response.json()
        validate(instance=obj, schema=AUTH_OBJECT_SCHEMA)
        auth_api.delete_object(obj["id"])

    def test_create_object_has_correct_name(self, auth_api):
        response = auth_api.create(AUTH_CREATE_DEVICE)
        obj = response.json()
        assert obj["name"] == AUTH_CREATE_DEVICE["name"]
        auth_api.delete_object(obj["id"])

    def test_created_object_is_retrievable(self, auth_api):
        """After POST, the new object must be fetchable via GET."""
        create_response = auth_api.create(AUTH_CREATE_DEVICE)
        obj_id = create_response.json()["id"]
        get_response = auth_api.get_by_id(obj_id)
        assert get_response.status_code == 200
        assert get_response.json()["id"] == obj_id
        auth_api.delete_object(obj_id)
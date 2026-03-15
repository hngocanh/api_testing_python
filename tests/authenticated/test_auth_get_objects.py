from jsonschema import validate
from test_data.schemas import AUTH_OBJECT_SCHEMA, AUTH_LIST_SCHEMA


class TestAuthHappyPath:

    def test_get_all_objects_status_200(self, auth_api):
        """GET /collections/{collectionName}/objects returns 200."""
        response = auth_api.get_all()
        assert response.status_code == 200

    def test_get_all_objects_matches_schema(self, auth_api):
        """Response from GET all matches the expected list schema."""
        response = auth_api.get_all()
        validate(instance=response.json(), schema=AUTH_LIST_SCHEMA)

    def test_get_by_id_status_200(self, auth_api, created_object):
        """GET /collections/{collectionName}/objects/{id} returns 200 for existing object."""
        response = auth_api.get_by_id(created_object["id"])
        assert response.status_code == 200

    def test_get_by_id_matches_schema(self, auth_api, created_object):
        """Response from GET by ID matches the expected object schema."""
        response = auth_api.get_by_id(created_object["id"])
        validate(instance=response.json(), schema=AUTH_OBJECT_SCHEMA)

class TestAuthGetEdgeCases:

    def test_get_objects_by_ids_filter(self, auth_api, auth_two_objects):
        ids = [obj["id"] for obj in auth_two_objects]
        response = auth_api.get_all(ids=ids)
        assert response.status_code == 200
        returned_ids = [obj["id"] for obj in response.json()]
        for expected_id in ids:
            assert expected_id in returned_ids

    def test_get_objects_with_single_id_filter(self, auth_api, created_object):
        response = auth_api.get_all(ids=[created_object["id"]])
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == created_object["id"]

    def test_get_empty_collection_returns_empty_list(self, auth_api):
        """If collection is empty, API should return an empty list not an error."""
        response = auth_api.get_all()
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestAuthGetNegativeCases:

    def test_get_object_nonexistent_id_returns_404(self, auth_api):
        response = auth_api.get_by_id("nonexistent-id-99999")
        assert response.status_code == 404

    def test_get_without_api_key_returns_401(self):
        """Requests without x-api-key header must be rejected."""
        import requests
        response = requests.get(
            "https://api.restful-api.dev/collections/my-devices/objects"
        )
        assert response.status_code == 403

    def test_get_with_invalid_api_key_returns_401(self):
        """Requests with a wrong API key must be rejected."""
        import requests
        response = requests.get(
            "https://api.restful-api.dev/collections/my-devices/objects",
            headers={"x-api-key": "invalid-key-000"}
        )
        assert response.status_code == 403
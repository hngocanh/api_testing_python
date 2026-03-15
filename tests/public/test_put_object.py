import pytest
from jsonschema import validate
from test_data.payloads import (
    PUT_FULL_UPDATE,
    PUT_MINIMAL_UPDATE,
    PUT_SAME_VALUES,
    PUT_DIFFERENT_DATA_TYPES,
    PUT_NAME_ONLY,
    PUT_MISSING_NAME,
    PUT_EMPTY_PAYLOAD,
    PUT_WRONG_TYPES,
)
from test_data.schemas import PUT_RESPONSE_SCHEMA


# ─────────────────────────────────────────────
# HAPPY PATH
# ─────────────────────────────────────────────

class TestPutHappyPath:

    def test_full_update_returns_200(self, public_api, created_object):
        """A valid PUT with all fields returns 200."""
        response = public_api.update(created_object["id"], PUT_FULL_UPDATE)
        assert response.status_code == 200

    def test_full_update_response_matches_schema(self, public_api, created_object):
        """Response structure matches the expected PUT schema."""
        response = public_api.update(created_object["id"], PUT_FULL_UPDATE)
        validate(instance=response.json(), schema=PUT_RESPONSE_SCHEMA)

    def test_full_update_name_is_updated(self, public_api, created_object):
        """Response body reflects the new name sent in the payload."""
        response = public_api.update(created_object["id"], PUT_FULL_UPDATE)
        assert response.json()["name"] == PUT_FULL_UPDATE["name"]

    def test_full_update_data_is_updated(self, public_api, created_object):
        """Response body reflects the new data fields sent in the payload."""
        response = public_api.update(created_object["id"], PUT_FULL_UPDATE)
        assert response.json()["data"] == PUT_FULL_UPDATE["data"]

    def test_full_update_id_is_unchanged(self, public_api, created_object):
        """PUT must not change the object's ID."""
        original_id = created_object["id"]
        response = public_api.update(original_id, PUT_FULL_UPDATE)
        assert response.json()["id"] == original_id

    def test_full_update_returns_updated_at_timestamp(self, public_api, created_object):
        """Response includes an updatedAt timestamp after a PUT."""
        response = public_api.update(created_object["id"], PUT_FULL_UPDATE)
        assert "updatedAt" in response.json()
        assert response.json()["updatedAt"] is not None

    def test_update_is_persisted(self, public_api, created_object):
        """A subsequent GET returns the updated values, confirming persistence."""
        public_api.update(created_object["id"], PUT_FULL_UPDATE)
        get_response = public_api.get_by_id(created_object["id"])
        assert get_response.json()["name"] == PUT_FULL_UPDATE["name"]
        assert get_response.json()["data"] == PUT_FULL_UPDATE["data"]


# ─────────────────────────────────────────────
# EDGE CASES
# ─────────────────────────────────────────────

class TestPutEdgeCases:

    def test_update_with_null_data_returns_200(self, public_api, created_object):
        """PUT with data set to null is valid — the API allows it."""
        # Check if object was created successfully
        if "id" not in created_object:
            pytest.fail(f"Object creation failed: {created_object.get('error', 'Unknown error')}")
        response = public_api.update(created_object["id"], PUT_MINIMAL_UPDATE)
        assert response.status_code == 200

    def test_update_with_null_data_persists(self, public_api, created_object):
        """After setting data to null, a GET confirms it is stored as null."""
        public_api.update(created_object["id"], PUT_MINIMAL_UPDATE)
        if "id" not in created_object:
            pytest.fail(f"Object creation failed: {created_object.get('error', 'Unknown error')}")
        get_response = public_api.get_by_id(created_object["id"])
        assert get_response.json()["data"] is None

    def test_update_with_same_values_returns_200(self, public_api, created_object):
        """Sending identical values still returns 200 — idempotent behaviour."""
        if "id" not in created_object:
            pytest.fail(f"Object creation failed: {created_object.get('error', 'Unknown error')}")
        response = public_api.update(created_object["id"], PUT_SAME_VALUES)
        assert response.status_code == 200

    def test_update_with_same_values_does_not_change_data(self, public_api, created_object):
        """Re-sending existing values doesn't corrupt the stored object."""
        public_api.update(created_object["id"], PUT_SAME_VALUES)
        if "id" not in created_object:
            pytest.fail(f"Object creation failed: {created_object.get('error', 'Unknown error')}")
        get_response = public_api.get_by_id(created_object["id"])
        assert get_response.json()["name"] == PUT_SAME_VALUES["name"]

    def test_update_with_mixed_data_types_returns_200(self, public_api, created_object):
        """data field accepts integers, floats, booleans, nulls, and arrays."""
        if "id" not in created_object:
            pytest.fail(f"Object creation failed: {created_object.get('error', 'Unknown error')}")
        response = public_api.update(created_object["id"], PUT_DIFFERENT_DATA_TYPES)
        assert response.status_code == 200

    def test_update_with_mixed_data_types_persists(self, public_api, created_object):
        """Mixed data types in the data field are stored and returned correctly."""
        public_api.update(created_object["id"], PUT_DIFFERENT_DATA_TYPES)
        if "id" not in created_object:
            pytest.fail(f"Object creation failed: {created_object.get('error', 'Unknown error')}")
        get_response = public_api.get_by_id(created_object["id"])
        assert get_response.json()["data"] == PUT_DIFFERENT_DATA_TYPES["data"]

    def test_update_without_data_key_returns_200(self, public_api, created_object):
        """PUT with name only and no data key is accepted."""
        if "id" not in created_object:
            pytest.fail(f"Object creation failed: {created_object.get('error', 'Unknown error')}")
        response = public_api.update(created_object["id"], PUT_NAME_ONLY)
        assert response.status_code == 200

    def test_put_is_idempotent(self, public_api, created_object):
        """Calling PUT twice with the same payload produces the same result."""
        if "id" not in created_object:
            pytest.fail(f"Object creation failed: {created_object.get('error', 'Unknown error')}")
        first  = public_api.update(created_object["id"], PUT_FULL_UPDATE)
        second = public_api.update(created_object["id"], PUT_FULL_UPDATE)
        assert first.json()["name"] == second.json()["name"]
        assert first.json()["data"] == second.json()["data"]


# ─────────────────────────────────────────────
# NEGATIVE CASES
# ─────────────────────────────────────────────

class TestPutNegativeCases:

    def test_update_nonexistent_id_returns_404(self, public_api):
        """PUT on an ID that doesn't exist returns 404."""
        response = public_api.update("nonexistent-id-99999", PUT_FULL_UPDATE)
        assert response.status_code == 404

    def test_update_with_missing_name_returns_error(self, public_api, created_object):
        """PUT without the required name field returns a 4xx error."""
        response = public_api.update(created_object["id"], PUT_MISSING_NAME)
        assert response.status_code in [400, 422]

    def test_update_with_empty_payload_returns_error(self, public_api, created_object):
        """PUT with a completely empty body returns a 4xx error."""
        response = public_api.update(created_object["id"], PUT_EMPTY_PAYLOAD)
        assert response.status_code in [400, 422]

    def test_update_with_wrong_name_type_returns_error(self, public_api, created_object):
        """PUT with name as an integer instead of string returns a 4xx error."""
        response = public_api.update(created_object["id"], PUT_WRONG_TYPES)
        assert response.status_code in [400, 422]

    def test_update_deleted_object_returns_404(self, public_api, created_object):
        """PUT on a deleted object returns 404."""
        object_id = created_object["id"]
        public_api.delete_object(object_id)
        response = public_api.update(object_id, PUT_FULL_UPDATE)
        assert response.status_code == 404
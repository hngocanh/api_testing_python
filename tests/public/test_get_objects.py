def test_get_all_object_status_200(public_api):
    response = public_api.get_all()
    assert response.status_code == 200

def test_get_all_objects_returns_list(public_api):
    response = public_api.get_all()
    assert isinstance(response.json(), list)

def test_get_single_object_status_200(public_api):
    response = public_api.get_by_id("7")
    assert response.status_code == 200

def test_get_single_object_has_correct_id(public_api):
    response = public_api.get_by_id("7")
    assert response.json()["id"] == "7"

def test_get_nonexistent_object_returns_404(public_api):
    response = public_api.get_by_id("999999")
    assert response.status_code == 404
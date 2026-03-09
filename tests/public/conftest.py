import pytest
from api.public.object_api import PublicObjectAPI
from test_data.payloads import CREATE_DEVICE

@pytest.fixture(scope="session")
def public_api():
    return PublicObjectAPI()

@pytest.fixture
def created_object(public_api):
    response = public_api.create(CREATE_DEVICE)
    obj = response.json()
    yield obj
    public_api.delete_object(obj["id"])
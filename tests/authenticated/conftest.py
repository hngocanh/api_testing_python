import pytest
from api.authenticated.auth_client import AuthClient
from api.authenticated.object_api import AuthenticatedObjectAPI
from utils.exceptions import RateLimitExceededException
from test_data.payloads import AUTH_CREATE_DEVICE, AUTH_CREATE_SECOND_DEVICE

_rate_limit_hit = False

def pytest_runtest_makereport(item, call):
    global _rate_limit_hit
    if call.excinfo is not None:
        if isinstance(call.excinfo.value, RateLimitExceededException):
            _rate_limit_hit = True

@pytest.fixture(autouse=True)
def skip_if_rate_limited():
    """
    Automatically skips every test once the rate limit has been hit.
    autouse=True means this runs for every test without needing to be declared.
    """
    if _rate_limit_hit:
        pytest.skip("Skipped — daily API limit already reached this session.")

@pytest.fixture(scope="session")
def auth_client():
    return AuthClient()

@pytest.fixture(scope="session")
def auth_api():
    return AuthenticatedObjectAPI()

@pytest.fixture
def created_object(auth_api):
    try:
        response = auth_api.create(AUTH_CREATE_DEVICE)
        obj = response.json()
    except RateLimitExceededException:
        pytest.skip("Skipped — rate limit hit during test setup (object creation).")

    yield obj

    try:
        auth_api.delete_object(obj["id"])
    except RateLimitExceededException:
        pass  # Object may already be gone — cleanup failure is acceptable

@pytest.fixture
def auth_two_objects(auth_api):
    """Creates two objects — used for tests that need to filter by ID."""
    created = []
    try:
        for payload in [AUTH_CREATE_DEVICE, AUTH_CREATE_SECOND_DEVICE]:
            response = auth_api.create(payload)
            created.append(response.json())
    except RateLimitExceededException:
        pytest.skip("Skipped — rate limit hit during multi-object creation.")

    yield created

    for obj in created:
        try:
            auth_api.delete_object(obj["id"])
        except Exception:
            pass
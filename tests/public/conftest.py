import pytest
from api.public.object_api import PublicObjectAPI
from test_data.payloads import CREATE_DEVICE
from utils.exceptions import RateLimitExceededException

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
def public_api():
    return PublicObjectAPI()

@pytest.fixture
def created_object(public_api):
    try:
        response = public_api.create(CREATE_DEVICE)
        obj = response.json()
    except RateLimitExceededException:
        pytest.skip("Skipped — rate limit hit during test setup (object creation).")

    yield obj

    try:
        public_api.delete_object(obj["id"])
    except RateLimitExceededException:
        pass  # Object may already be gone — cleanup failure is acceptable
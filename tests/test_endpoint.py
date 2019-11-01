import pytest
from restfly.endpoint import APIEndpoint

@pytest.fixture
def e(api):
    return APIEndpoint(api)

def validate_endpoint(e, api):
    assert e._api == api
    assert e._log == api._log
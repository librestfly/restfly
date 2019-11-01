import pytest
from restfly.session import APISession

@pytest.fixture
def api():
    return APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build='b01',
    )
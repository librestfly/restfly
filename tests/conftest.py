import pytest
from restfly.session import APISession
from restfly import __version__ as version

@pytest.fixture
def api():
    return APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build=version,
    )
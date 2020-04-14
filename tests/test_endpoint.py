import pytest
from requests import Request, Response
from restfly.endpoint import APIEndpoint

@pytest.fixture
def e(api):
    return APIEndpoint(api)

def validate_endpoint(e, api):
    assert e._api == api
    assert e._log == api._log

@pytest.mark.vcr()
def test_endpoint_delete(e):
    resp = e._delete('delete', json={'test': 'value'})
    assert isinstance(resp, Response)

@pytest.mark.vcr()
def test_endpoint_get(e):
    resp = e._get('get', json={'test': 'value'})
    assert isinstance(resp, Response)

@pytest.mark.vcr()
def test_endpoint_patch(e):
    resp = e._patch('patch', json={'test': 'value'})
    assert isinstance(resp, Response)

@pytest.mark.vcr()
def test_endpoint_post(e):
    resp = e._post('post', json={'test': 'value'})
    assert isinstance(resp, Response)

@pytest.mark.vcr()
def test_endpoint_put(e):
    resp = e._put('put', json={'test': 'value'})
    assert isinstance(resp, Response)

@pytest.mark.vcr()
def test_endpoint_base_request(e):
    resp = e._request('PUT', 'put', json={'test': 'value'})
    assert isinstance(resp, Response)

@pytest.mark.vcr()
def test_endpoint_path_get(api):
    class TestAPI(APIEndpoint):
        _path = 'get'
        def get(self):
            return self._get()
    endpoint = TestAPI(api)
    resp = endpoint.get()
    assert isinstance(resp, Response)
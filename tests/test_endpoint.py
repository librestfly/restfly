import pytest
import responses
from requests import Response
from box import Box
from restfly.endpoint import APIEndpoint


@pytest.fixture
def e(api):
    return APIEndpoint(api)


def validate_endpoint(e, api):
    assert e._api == api
    assert e._log == api._log


@responses.activate
def test_endpoint_delete(e):
    responses.add(responses.DELETE, 'https://httpbin.org/delete')
    resp = e._delete('delete', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_head(e):
    responses.add(responses.HEAD, 'https://httpbin.org')
    resp = e._head('')
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_get(e):
    responses.add(responses.GET, 'https://httpbin.org/get')
    resp = e._get('get', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_patch(e):
    responses.add(responses.PATCH, 'https://httpbin.org/patch')
    resp = e._patch('patch', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_post(e):
    responses.add(responses.POST, 'https://httpbin.org/post')
    resp = e._post('post', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_put(e):
    responses.add(responses.PUT, 'https://httpbin.org/put')
    resp = e._put('put', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_endpoint_base_request(e):
    responses.add(responses.PUT, 'https://httpbin.org/put', json={'test': 'value'})
    resp = e._req('PUT', 'put', json={'test': 'value'})
    assert isinstance(resp, Response)

    # Test endpoint params:
    e._box = True
    e._box_attrs = {'default_box': True}
    assert isinstance(e._req('PUT', 'put', json={'test': 'value'}), Box)

    e._box = None
    e._conv_json = True
    assert isinstance(e._req('PUT', 'put', json={'test': 'value'}), dict)


@responses.activate
def test_endpoint_path_get(api):
    responses.add(responses.GET, 'https://httpbin.org/get')

    class TestAPI(APIEndpoint):
        _path = 'get'

        def get(self):
            return self._get()

    endpoint = TestAPI(api)
    resp = endpoint.get()
    assert isinstance(resp, Response)

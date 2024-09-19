import pytest
import logging
import responses
from requests import Response
from requests.adapters import HTTPAdapter
from requests.exceptions import SSLError
from urllib3.exceptions import InsecureRequestWarning
from urllib3.util.retry import Retry
from box import Box, BoxList
from restfly import __version__ as version, APISession
from restfly import errors


def test_error_repr():
    err = errors.RestflyException('This is a test')
    assert str(err) == 'This is a test'
    assert err.__repr__() == "'This is a test'"


def test_retriable_error():
    assert errors.APIError.retryable == False
    errors.APIError.set_retryable(True)
    assert errors.APIError.retryable == True
    errors.APIError.set_retryable(False)
    assert errors.APIError.retryable == False


def test_user_agent_string(api):
    ua = 'Integration/1.0 (pytest; auto-test; Build/{version})'.format(version=version)
    assert ua in api._session.headers['User-Agent']


def test_unexpected_keys_error():
    class Example1(APISession):
        _error_on_unexpected_input = True
        _url = 'https://httpbin.org'

    class Example2(APISession):
        _error_on_unexpected_input = False
        _url = 'https://httpbin.org'

    # should raise an error with the invalid KW
    with pytest.raises(errors.UnexpectedValueError):
        Example1(something=True)

    # Should not raise the error and just ignore it.
    Example2(something=True)


def test_example_context_manager():
    """
    This test creates a simple "authentication" to validate that the
    context management is actually working as expected.  As the _authenticate
    method is automatically run when entering the context, and _deauthenticate
    is run upon exit, we will simply be modifying the authed variable in the
    outer scope and asserting that its being properly set.
    """
    global authed

    class Example(APISession):
        _url = 'https://httpbin.org'

        def _authenticate(self, **kwargs):
            global authed
            authed = True

        def _deauthenticate(self):
            global authed
            authed = False

    with Example():
        assert authed is True
    assert authed is False


def test_session_proxies():
    api = APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build=version,
        proxies={'http': 'localhost:8080'},
    )
    assert api._session.proxies == {'http': 'localhost:8080'}


def test_session_ssl_validation():
    api = APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build=version,
        ssl_verify=False,
    )
    assert api._session.verify is False


def test_client_ssl_cert():
    cert_tuple = ('/path/to/cert.crt', '/path/to/cert.key')
    api = APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build=version,
        cert=cert_tuple,
    )
    assert api._session.cert == cert_tuple


def test_session_adapter():
    retry = Retry(
        total=5,
        read=5,
        connect=5,
        backoff_factor=5,
    )
    adapter = HTTPAdapter(max_retries=retry)
    api = APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build=version,
        adapter=adapter,
    )
    assert api._session.get_adapter('https://httpbin.org/') == adapter


def test_session_stubs(api):
    api._authenticate()
    api._deauthenticate()


@responses.activate
def test_session_delete(api):
    responses.add(responses.DELETE, 'https://httpbin.org/delete')
    resp = api.delete('delete', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_session_get(api):
    responses.add(responses.GET, 'https://httpbin.org/get')
    resp = api.get('get', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_session_patch(api):
    responses.add(responses.PATCH, 'https://httpbin.org/patch')
    resp = api.patch('patch', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_session_post(api):
    responses.add(responses.POST, 'https://httpbin.org/post')
    resp = api.post('post', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_session_put(api):
    responses.add(responses.PUT, 'https://httpbin.org/put')
    resp = api.put('put', json={'test': 'value'})
    assert isinstance(resp, Response)


@responses.activate
def test_session_head(api):
    responses.add(responses.HEAD, 'https://httpbin.org/')
    resp = api.head('')
    assert isinstance(resp, Response)


@responses.activate
def test_session_redirect(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/redirect-to',
        status=302,
        headers={'Location': '/get'},
    )
    responses.add(responses.GET, 'https://httpbin.org/get')
    resp = api.get('redirect-to', params={'url': '/get'})
    assert isinstance(resp, Response)
    assert resp.url == 'https://httpbin.org/get'


@responses.activate
def test_debug_logging(api, caplog):
    data = {'a': 1, 'b': 2, 'c': {'d': 3, 'e': 4}}
    responses.add(responses.POST, 'https://httpbin.org/post', json={'json': data})
    caplog.clear()
    with caplog.at_level(logging.DEBUG, logger='restfly.session.APISession'):
        resp = api.post('post', json=data, redact_fields=['a', 'd'], box=False)
        assert '"a": "REDACTED"' in caplog.text
        assert '"d": "REDACTED"' in caplog.text
        assert resp.json()['json'] == data

    caplog.clear()
    with caplog.at_level(logging.DEBUG, logger='restfly.session.APISession'):
        api._restricted_paths = ['post']
        resp = api.post('post', json=data, redact_fields=['a', 'd'], box=False)
        api._restricted_paths = []
        assert '"params": "REDACTED"' in caplog.text
        assert '"body": "REDACTED"' in caplog.text
        assert resp.json()['json'] == data

    caplog.clear()
    with caplog.at_level(logging.DEBUG, logger='restfly.session.APISession'):
        resp = api.post('post', json=data, box=False)
        assert 'REDACTED' not in caplog.text
        assert resp.json()['json'] == data


@responses.activate
def test_session_full_uri(api):
    responses.add(responses.GET, 'https://httpbin.org/get', json={'test': 'value'})
    resp1 = api.get('get').json()
    resp2 = api.get('https://httpbin.org/get').json()
    assert resp1 == resp2


@responses.activate
def test_session_base_path(api):
    responses.add(
        responses.POST, 'https://httpbin.org/post', json={'data': {'test': 'value'}}
    )
    resp1 = api.post('post', json={'test': 'value'}).json()
    api._base_path = 'get'
    resp2 = api.post('post', json={'test': 'value'}, use_base=False).json()
    resp1['headers'] = {}
    resp2['headers'] = {}
    assert resp1 == resp2

    responses.add(responses.GET, 'https://httpbin.org/status/200')
    api._base_path = 'status'
    api.get('200')


@responses.activate
def test_session_retry_after(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/response-headers',
        headers={'Retry-After': '.1'},
    )
    api.get('response-headers', params={'Retry-After': 1})


def test_session_ssl_error(api):
    with pytest.raises(SSLError):
        api.get('https://self-signed.badssl.com/')
    api._ssl_verify = False
    with pytest.warns(InsecureRequestWarning):
        api.get('https://self-signed.badssl.com/')


@responses.activate
def test_session_badrequesterror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/400', status=400)
    with pytest.raises(errors.BadRequestError):
        api.get('status/400')


@responses.activate
def test_session_unauthorizederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/401', status=401)
    with pytest.raises(errors.UnauthorizedError):
        api.get('status/401')


@responses.activate
def test_session_forbiddenerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/403', status=403)
    with pytest.raises(errors.ForbiddenError):
        api.get('status/403')


@responses.activate
def test_session_notfounderror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/404', status=404)
    with pytest.raises(errors.NotFoundError):
        api.get('status/404')


@responses.activate
def test_session_invalidmethoderror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/405', status=405)
    with pytest.raises(errors.InvalidMethodError):
        api.get('status/405')


@responses.activate
def test_session_notacceptableerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/406', status=406)
    with pytest.raises(errors.NotAcceptableError):
        api.get('status/406')


@responses.activate
def test_session_proxyauthenticationerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/407', status=407)
    with pytest.raises(errors.ProxyAuthenticationError):
        api.get('status/407')


@responses.activate
def test_session_requesttimeouterror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/408', status=408)
    with pytest.raises(errors.RequestTimeoutError):
        api.get('status/408')


@responses.activate
def test_session_requestconflicterror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/409', status=409)
    with pytest.raises(errors.RequestConflictError):
        api.get('status/409')


@responses.activate
def test_session_nolongerexistserror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/410', status=410)
    with pytest.raises(errors.NoLongerExistsError):
        api.get('status/410')


@responses.activate
def test_session_lengthrequirederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/411', status=411)
    with pytest.raises(errors.LengthRequiredError):
        api.get('status/411')


@responses.activate
def test_session_preconditionfailederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/412', status=412)
    with pytest.raises(errors.PreconditionFailedError):
        api.get('status/412')


@responses.activate
def test_session_payloadtoolargeerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/413', status=413)
    with pytest.raises(errors.PayloadTooLargeError):
        api.get('status/413')


@responses.activate
def test_session_uritoolongerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/414', status=414)
    with pytest.raises(errors.URITooLongError):
        api.get('status/414')


@responses.activate
def test_session_unsupportedmediatypeerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/415', status=415)
    with pytest.raises(errors.UnsupportedMediaTypeError):
        api.get('status/415')


@responses.activate
def test_session_rangenotsatisfiableerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/416', status=416)
    with pytest.raises(errors.RangeNotSatisfiableError):
        api.get('status/416')


@responses.activate
def test_session_expectationfailederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/417', status=417)
    with pytest.raises(errors.ExpectationFailedError):
        api.get('status/417')


@responses.activate
def test_session_teapotresponseerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/418', status=418)
    with pytest.raises(errors.TeapotResponseError):
        api.get('status/418')


@responses.activate
def test_session_misdirectrequesterror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/421', status=421)
    with pytest.raises(errors.MisdirectRequestError):
        api.get('status/421')


@responses.activate
def test_session_tooearlyerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/425', status=425)
    with pytest.raises(errors.TooEarlyError):
        api.get('status/425')


@responses.activate
def test_session_upgraderequirederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/426', status=426)
    with pytest.raises(errors.UpgradeRequiredError):
        api.get('status/426')


@responses.activate
def test_session_preconditionrequirederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/428', status=428)
    with pytest.raises(errors.PreconditionRequiredError):
        api.get('status/428')


@responses.activate
def test_session_toomanyrequests(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/status/429',
        status=429,
        headers={'Retry-After': '.1'},
    )
    with pytest.raises(errors.TooManyRequestsError):
        api.get('status/429')


@responses.activate
def test_session_requestheaderfieldstoolargeerror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/431', status=431)
    with pytest.raises(errors.RequestHeaderFieldsTooLargeError):
        api.get('status/431')


@responses.activate
def test_session_unavailableforlegalreasonserror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/451', status=451)
    with pytest.raises(errors.UnavailableForLegalReasonsError):
        api.get('status/451')


@responses.activate
def test_session_servererror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/500', status=500)
    with pytest.raises(errors.ServerError):
        api.get('status/500')


@responses.activate
def test_session_methodnotimplimentederror(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/status/501',
        status=501,
        headers={'Retry-After': '.1'},
    )
    with pytest.raises(errors.MethodNotImplementedError):
        api.get('status/501')


@responses.activate
def test_session_badgatewayerror(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/status/502',
        status=502,
        headers={'Retry-After': '.1'},
    )
    with pytest.raises(errors.BadGatewayError):
        api.get('status/502')


@responses.activate
def test_session_serviceunavailableerror(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/status/503',
        status=503,
        headers={'Retry-After': '.1'},
    )
    with pytest.raises(errors.ServiceUnavailableError):
        api.get('status/503')


@responses.activate
def test_session_gatewaytimeouterror(api):
    responses.add(
        responses.GET,
        'https://httpbin.org/status/504',
        status=504,
        headers={'Retry-After': '.1'},
    )
    with pytest.raises(errors.GatewayTimeoutError):
        api.get('status/504')


@responses.activate
def test_session_notextendederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/510', status=510)
    with pytest.raises(errors.NotExtendedError):
        api.get('status/510')


@responses.activate
def test_session_networkauthrequirederror(api):
    responses.add(responses.GET, 'https://httpbin.org/status/511', status=511)
    with pytest.raises(errors.NetworkAuthenticationRequiredError):
        api.get('status/511')


@responses.activate
def test_session_catchall_error(api):
    responses.add(responses.GET, 'https://httpbin.org/status/555', status=555)
    with pytest.raises(errors.APIError):
        api.get('status/555')


@responses.activate
def test_session_box_non_json(api):
    html_body = '<html><head></head><body><h1>Hello World</h1></body></html>'
    responses.add(
        responses.GET,
        'https://httpbin.org/html',
        headers={'Content-Type': 'text/html; charset=utf-8'},
        body=html_body,
    )
    assert isinstance(api.get('html', box=True), Response)


@responses.activate
def test_session_box_json(api):
    responses.add(responses.GET, 'https://httpbin.org/json', json={'test': 'value'})
    assert isinstance(api.get('json', box=True), Box)
    responses.add(
        responses.GET,
        'https://httpbin.org/json',
        json=[{'test': 'value'} for _ in range(20)],
    )
    assert isinstance(api.get('json', box=True), BoxList)


@responses.activate
def test_session_disable_box(api):
    responses.add(responses.GET, 'https://httpbin.org/json', json={'test': 'value'})
    assert isinstance(api.get('json', box=False), Response)


@responses.activate
def test_session_conv_json_non_json(api):
    html_body = '<html><head></head><body><h1>Hello World</h1></body></html>'
    responses.add(
        responses.GET,
        'https://httpbin.org/html',
        headers={'Content-Type': 'text/html; charset=utf-8'},
        body=html_body,
    )
    assert isinstance(api.get('html', conv_json=True), Response)


@responses.activate
def test_session_conv_json_json(api):
    responses.add(responses.GET, 'https://httpbin.org/json', json={'test': 'value'})
    assert isinstance(api.get('json', conv_json=True), dict)


@responses.activate
def test_session_disable_conv_json(api):
    responses.add(responses.GET, 'https://httpbin.org/json', json={'test': 'value'})
    assert isinstance(api.get('json', conv_json=False), Response)

import pytest
import logging
from requests import Response
from requests.exceptions import SSLError
from urllib3.exceptions import InsecureRequestWarning
from box import Box
from restfly import __version__ as version, APISession
from restfly import errors


def test_error_repr():
    err = errors.RestflyException('This is a test')
    assert str(err) == 'This is a test'
    assert err.__repr__() == "'This is a test'"


def test_user_agent_string(api):
    ua = 'Integration/1.0 (pytest; auto-test; Build/{version})'.format(
        version=version
    )
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
    '''
    This test creates a simple "authentication" to validate that the
    context management is actually working as expected.  As the _authenticate
    method is automatically run when entering the context, and _deauthenticate
    is run upon exit, we will simply be modifying the authed variable in the
    outer scope and asserting that its being properly set.
    '''
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
        proxies={'http': 'localhost:8080'}
    )
    assert api._session.proxies == {'http': 'localhost:8080'}


def test_session_ssl_validation():
    api = APISession(
        url='https://httpbin.org',
        vendor='pytest',
        product='auto-test',
        build=version,
        ssl_verify=False
    )
    assert api._session.verify is False


def test_session_stubs(api):
    api._authenticate()
    api._deauthenticate()


@pytest.mark.vcr()
@pytest.mark.skip('No HTTPBin HEAD Verb to test against')
def test_session_head(api):
    resp = api.head('delete', json={'test': 'value'})
    assert isinstance(resp, Response)


@pytest.mark.vcr()
def test_session_delete(api):
    resp = api.delete('delete', json={'test': 'value'})
    assert isinstance(resp, Response)


@pytest.mark.vcr()
def test_session_get(api):
    resp = api.get('get', json={'test': 'value'})
    assert isinstance(resp, Response)


@pytest.mark.vcr()
def test_session_patch(api):
    resp = api.patch('patch', json={'test': 'value'})
    assert isinstance(resp, Response)


@pytest.mark.vcr()
def test_session_post(api):
    resp = api.post('post', json={'test': 'value'})
    assert isinstance(resp, Response)


@pytest.mark.vcr()
def test_session_put(api):
    resp = api.put('put', json={'test': 'value'})
    assert isinstance(resp, Response)


@pytest.mark.vcr()
def test_session_head(api):
    resp = api.head('')
    assert isinstance(resp, Response)


@pytest.mark.vcr()
def test_session_redirect(api):
    resp = api.get('redirect-to', params={'url': '/get'})
    assert isinstance(resp, Response)


@pytest.mark.vcr()
def test_debug_logging(api, caplog):
    data = {'a': 1, 'b': 2, 'c': {'d': 3, 'e': 4}}
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

    caplog.clear()
    with caplog.at_level(logging.DEBUG, logger='restfly.session.APISession'):
        resp = api.post('post',
                        json=data,
                        box=True,
                        box_attrs={'default_box': True}
                        )
        assert 'unknown attrs will return as' in caplog.text


@pytest.mark.vcr()
def test_session_full_uri(api):
    resp1 = api.get('get', json={'test': 'value'}).json()
    resp2 = api.get('https://httpbin.org/get', json={'test': 'value'}).json()
    assert resp1 == resp2


@pytest.mark.vcr()
def test_session_base_path(api):
    resp1 = api.post('post', json={'test': 'value'}).json()
    api._base_path = 'get'
    resp2 = api.post('post', json={'test': 'value'}, use_base=False).json()
    resp1['headers'] = {}
    resp2['headers'] = {}
    assert resp1 == resp2
    api._base_path = 'status'
    api.get('200')


@pytest.mark.vcr()
def test_session_retry_after(api):
    api.get('response-headers', params={
        'Retry-After': 1
    })


def test_session_ssl_error(api):
    with pytest.raises(SSLError):
        api.get('https://self-signed.badssl.com/')
    api._ssl_verify = False
    with pytest.warns(InsecureRequestWarning):
        api.get('https://self-signed.badssl.com/')


@pytest.mark.vcr()
def test_session_badrequesterror(api):
    with pytest.raises(errors.BadRequestError):
        api.get('status/400')


@pytest.mark.vcr()
def test_session_unauthorizederror(api):
    with pytest.raises(errors.UnauthorizedError):
        api.get('status/401')


@pytest.mark.vcr()
def test_session_forbiddenerror(api):
    with pytest.raises(errors.ForbiddenError):
        api.get('status/403')


@pytest.mark.vcr()
def test_session_notfounderror(api):
    with pytest.raises(errors.NotFoundError):
        api.get('status/404')


@pytest.mark.vcr()
def test_session_invalidmethoderror(api):
    with pytest.raises(errors.InvalidMethodError):
        api.get('status/405')


@pytest.mark.vcr()
def test_session_notacceptableerror(api):
    with pytest.raises(errors.NotAcceptableError):
        api.get('status/406')


@pytest.mark.vcr()
def test_session_proxyauthenticationerror(api):
    with pytest.raises(errors.ProxyAuthenticationError):
        api.get('status/407')


@pytest.mark.vcr()
def test_session_requesttimeouterror(api):
    with pytest.raises(errors.RequestTimeoutError):
        api.get('status/408')


@pytest.mark.vcr()
def test_session_requestconflicterror(api):
    with pytest.raises(errors.RequestConflictError):
        api.get('status/409')


@pytest.mark.vcr()
def test_session_nolongerexistserror(api):
    with pytest.raises(errors.NoLongerExistsError):
        api.get('status/410')


@pytest.mark.vcr()
def test_session_lengthrequirederror(api):
    with pytest.raises(errors.LengthRequiredError):
        api.get('status/411')


@pytest.mark.vcr()
def test_session_preconditionfailederror(api):
    with pytest.raises(errors.PreconditionFailedError):
        api.get('status/412')


@pytest.mark.vcr()
def test_session_payloadtoolargeerror(api):
    with pytest.raises(errors.PayloadTooLargeError):
        api.get('status/413')


@pytest.mark.vcr()
def test_session_uritoolongerror(api):
    with pytest.raises(errors.URITooLongError):
        api.get('status/414')


@pytest.mark.vcr()
def test_session_unsupportedmediatypeerror(api):
    with pytest.raises(errors.UnsupportedMediaTypeError):
        api.get('status/415')


@pytest.mark.vcr()
def test_session_rangenotsatisfiableerror(api):
    with pytest.raises(errors.RangeNotSatisfiableError):
        api.get('status/416')


@pytest.mark.vcr()
def test_session_expectationfailederror(api):
    with pytest.raises(errors.ExpectationFailedError):
        api.get('status/417')


@pytest.mark.vcr()
def test_session_teapotresponseerror(api):
    with pytest.raises(errors.TeapotResponseError):
        api.get('status/418')


@pytest.mark.vcr()
def test_session_misdirectrequesterror(api):
    with pytest.raises(errors.MisdirectRequestError):
        api.get('status/421')


@pytest.mark.vcr()
def test_session_tooearlyerror(api):
    with pytest.raises(errors.TooEarlyError):
        api.get('status/425')


@pytest.mark.vcr()
def test_session_upgraderequirederror(api):
    with pytest.raises(errors.UpgradeRequiredError):
        api.get('status/426')


@pytest.mark.vcr()
def test_session_preconditionrequirederror(api):
    with pytest.raises(errors.PreconditionRequiredError):
        api.get('status/428')


@pytest.mark.vcr()
def test_session_toomanyrequests(api):
    with pytest.raises(errors.TooManyRequestsError):
        api.get('status/429')


@pytest.mark.vcr()
def test_session_requestheaderfieldstoolargeerror(api):
    with pytest.raises(errors.RequestHeaderFieldsTooLargeError):
        api.get('status/431')


@pytest.mark.vcr()
def test_session_unavailableforlegalreasonserror(api):
    with pytest.raises(errors.UnavailableForLegalReasonsError):
        api.get('status/451')


@pytest.mark.vcr()
def test_session_servererror(api):
    with pytest.raises(errors.ServerError):
        api.get('status/500')


@pytest.mark.vcr()
def test_session_methodnotimplimentederror(api):
    with pytest.raises(errors.MethodNotImplementedError):
        api.get('status/501')


@pytest.mark.vcr()
def test_session_badgatewayerror(api):
    with pytest.raises(errors.BadGatewayError):
        api.get('status/502')


@pytest.mark.vcr()
def test_session_serviceunavailableerror(api):
    with pytest.raises(errors.ServiceUnavailableError):
        api.get('status/503')


@pytest.mark.vcr()
def test_session_gatewaytimeouterror(api):
    with pytest.raises(errors.GatewayTimeoutError):
        api.get('status/504')


@pytest.mark.vcr()
def test_session_notextendederror(api):
    with pytest.raises(errors.NotExtendedError):
        api.get('status/510')


@pytest.mark.vcr()
def test_session_networkauthrequirederror(api):
    with pytest.raises(errors.NetworkAuthenticationRequiredError):
        api.get('status/511')


@pytest.mark.vcr()
def test_session_catchall_error(api):
    with pytest.raises(errors.APIError):
        api.get('status/555')


@pytest.mark.vcr()
def test_session_box_non_json(api):
    assert isinstance(api.get('html', box=True), Response)


@pytest.mark.vcr()
def test_session_box_json(api):
    assert isinstance(api.get('json', box=True), Box)


@pytest.mark.vcr()
def test_session_disable_box(api):
    assert isinstance(api.get('json', box=False), Response)


@pytest.mark.vcr()
def test_session_conv_json_non_json(api):
    assert isinstance(api.get('html', conv_json=True), Response)


@pytest.mark.vcr()
def test_session_conv_json_json(api):
    assert isinstance(api.get('json', conv_json=True), dict)


@pytest.mark.vcr()
def test_session_disable_conv_json(api):
    assert isinstance(api.get('json', conv_json=False), Response)

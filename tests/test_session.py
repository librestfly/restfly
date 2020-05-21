import pytest, sys
from requests import Request, Response
from box import Box
from restfly import __version__ as version, APISession
from restfly.errors import *

def test_user_agent_string(api):
    ua = 'Integration/1.0 (pytest; auto-test; Build/{version})'.format(
        version=version
    )
    assert ua in api._session.headers['User-Agent']

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

    with Example() as ex:
        assert authed == True
    assert authed == False

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
def test_session_redirect(api):
    resp = api.get('redirect-to', params={'url': '/get'})
    assert isinstance(resp, Response)

@pytest.mark.vcr()
def test_session_full_uri(api):
    resp1 = api.get('get', json={'test': 'value'}).json()
    resp2 = api.get('https://httpbin.org/get', json={'test': 'value'}).json()
    assert resp1 == resp2

@pytest.mark.vcr()
def test_session_badrequesterror(api):
    with pytest.raises(BadRequestError):
        api.get('status/400')

@pytest.mark.vcr()
def test_session_unauthorizederror(api):
    with pytest.raises(UnauthorizedError):
        api.get('status/401')

@pytest.mark.vcr()
def test_session_forbiddenerror(api):
    with pytest.raises(ForbiddenError):
        api.get('status/403')

@pytest.mark.vcr()
def test_session_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.get('status/404')

@pytest.mark.vcr()
def test_session_invalidmethoderror(api):
    with pytest.raises(InvalidMethodError):
        api.get('status/405')

@pytest.mark.vcr()
def test_session_notacceptableerror(api):
    with pytest.raises(NotAcceptableError):
        api.get('status/406')

@pytest.mark.vcr()
def test_session_proxyauthenticationerror(api):
    with pytest.raises(ProxyAuthenticationError):
        api.get('status/407')

@pytest.mark.vcr()
def test_session_requesttimeouterror(api):
    with pytest.raises(RequestTimeoutError):
        api.get('status/408')

@pytest.mark.vcr()
def test_session_requestconflicterror(api):
    with pytest.raises(RequestConflictError):
        api.get('status/409')

@pytest.mark.vcr()
def test_session_nolongerexistserror(api):
    with pytest.raises(NoLongerExistsError):
        api.get('status/410')

@pytest.mark.vcr()
def test_session_lengthrequirederror(api):
    with pytest.raises(LengthRequiredError):
        api.get('status/411')

@pytest.mark.vcr()
def test_session_preconditionfailederror(api):
    with pytest.raises(PreconditionFailedError):
        api.get('status/412')

@pytest.mark.vcr()
def test_session_payloadtoolargeerror(api):
    with pytest.raises(PayloadTooLargeError):
        api.get('status/413')

@pytest.mark.vcr()
def test_session_uritoolongerror(api):
    with pytest.raises(URITooLongError):
        api.get('status/414')

@pytest.mark.vcr()
def test_session_unsupportedmediatypeerror(api):
    with pytest.raises(UnsupportedMediaTypeError):
        api.get('status/415')

@pytest.mark.vcr()
def test_session_rangenotsatisfiableerror(api):
    with pytest.raises(RangeNotSatisfiableError):
        api.get('status/416')

@pytest.mark.vcr()
def test_session_expectationfailederror(api):
    with pytest.raises(ExpectationFailedError):
        api.get('status/417')

@pytest.mark.vcr()
def test_session_teapotresponseerror(api):
    with pytest.raises(TeapotResponseError):
        api.get('status/418')

@pytest.mark.vcr()
def test_session_misdirectrequesterror(api):
    with pytest.raises(MisdirectRequestError):
        api.get('status/421')

@pytest.mark.vcr()
def test_session_tooearlyerror(api):
    with pytest.raises(TooEarlyError):
        api.get('status/425')

@pytest.mark.vcr()
def test_session_upgraderequirederror(api):
    with pytest.raises(UpgradeRequiredError):
        api.get('status/426')

@pytest.mark.vcr()
def test_session_preconditionrequirederror(api):
    with pytest.raises(PreconditionRequiredError):
        api.get('status/428')

@pytest.mark.vcr()
def test_session_toomanyrequests(api):
    with pytest.raises(TooManyRequestsError):
        api.get('status/429')

@pytest.mark.vcr()
def test_session_requestheaderfieldstoolargeerror(api):
    with pytest.raises(RequestHeaderFieldsTooLargeError):
        api.get('status/431')

@pytest.mark.vcr()
def test_session_unavailableforlegalreasonserror(api):
    with pytest.raises(UnavailableForLegalReasonsError):
        api.get('status/451')

@pytest.mark.vcr()
def test_session_servererror(api):
    with pytest.raises(ServerError):
        api.get('status/500')

@pytest.mark.vcr()
def test_session_methodnotimplimentederror(api):
    with pytest.raises(MethodNotImplementedError):
        api.get('status/501')

@pytest.mark.vcr()
def test_session_badgatewayerror(api):
    with pytest.raises(BadGatewayError):
        api.get('status/502')

@pytest.mark.vcr()
def test_session_serviceunavailableerror(api):
    with pytest.raises(ServiceUnavailableError):
        api.get('status/503')

@pytest.mark.vcr()
def test_session_gatewaytimeouterror(api):
    with pytest.raises(GatewayTimeoutError):
        api.get('status/504')

@pytest.mark.vcr()
def test_session_notextendederror(api):
    with pytest.raises(NotExtendedError):
        api.get('status/510')

@pytest.mark.vcr()
def test_session_networkauthrequirederror(api):
    with pytest.raises(NetworkAuthenticationRequiredError):
        api.get('status/511')

@pytest.mark.vcr()
def test_session_box_non_json(api):
    assert isinstance(api.get('html'), Response)

@pytest.mark.vcr()
def test_session_box_json(api):
    assert isinstance(api.get('json', box=True), Box)

@pytest.mark.vcr()
def test_session_disable_box(api):
    assert isinstance(api.get('json', box=False), Response)
import pytest
from requests import Request, Response
from restfly.errors import *

def test_session_delete(api):
    resp = api.delete('delete', json={'test': 'value'})
    assert isinstance(resp, Response)

def test_session_get(api):
    resp = api.get('get', json={'test': 'value'})
    assert isinstance(resp, Response)

def test_session_patch(api):
    resp = api.patch('patch', json={'test': 'value'})
    assert isinstance(resp, Response)

def test_session_post(api):
    resp = api.post('post', json={'test': 'value'})
    assert isinstance(resp, Response)

def test_session_put(api):
    resp = api.put('put', json={'test': 'value'})
    assert isinstance(resp, Response)

def test_session_redirect(api):
    resp = api.get('redirect-to', params={'url': '/get'})
    assert isinstance(resp, Response)

def test_session_badrequesterror(api):
    with pytest.raises(BadRequestError):
        api.get('status/400')

def test_session_unauthorizederror(api):
    with pytest.raises(UnauthorizedError):
        api.get('status/401')

def test_session_forbiddenerror(api):
    with pytest.raises(ForbiddenError):
        api.get('status/403')

def test_session_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.get('status/404')

def test_session_invalidmethoderror(api):
    with pytest.raises(InvalidMethodError):
        api.get('status/405')

def test_session_notacceptableerror(api):
    with pytest.raises(NotAcceptableError):
        api.get('status/406')

def test_session_proxyauthenticationerror(api):
    with pytest.raises(ProxyAuthenticationError):
        api.get('status/407')

def test_session_requesttimeouterror(api):
    with pytest.raises(RequestTimeoutError):
        api.get('status/408')

def test_session_requestconflicterror(api):
    with pytest.raises(RequestConflictError):
        api.get('status/409')

def test_session_nolongerexistserror(api):
    with pytest.raises(NoLongerExistsError):
        api.get('status/410')

def test_session_lengthrequirederror(api):
    with pytest.raises(LengthRequiredError):
        api.get('status/411')

def test_session_preconditionfailederror(api):
    with pytest.raises(PreconditionFailedError):
        api.get('status/412')

def test_session_payloadtoolargeerror(api):
    with pytest.raises(PayloadTooLargeError):
        api.get('status/413')

def test_session_uritoolongerror(api):
    with pytest.raises(URITooLongError):
        api.get('status/414')

def test_session_unsupportedmediatypeerror(api):
    with pytest.raises(UnsupportedMediaTypeError):
        api.get('status/415')

def test_session_rangenotsatisfiableerror(api):
    with pytest.raises(RangeNotSatisfiableError):
        api.get('status/416')

def test_session_expectationfailederror(api):
    with pytest.raises(ExpectationFailedError):
        api.get('status/417')

def test_session_teapotresponseerror(api):
    with pytest.raises(TeapotResponseError):
        api.get('status/418')

def test_session_misdirectrequesterror(api):
    with pytest.raises(MisdirectRequestError):
        api.get('status/421')

def test_session_tooearlyerror(api):
    with pytest.raises(TooEarlyError):
        api.get('status/425')

def test_session_upgraderequirederror(api):
    with pytest.raises(UpgradeRequiredError):
        api.get('status/426')

def test_session_preconditionrequirederror(api):
    with pytest.raises(PreconditionRequiredError):
        api.get('status/428')

def test_session_toomanyrequests(api):
    with pytest.raises(TooManyRequestsError):
        api.get('status/429')

def test_session_requestheaderfieldstoolargeerror(api):
    with pytest.raises(RequestHeaderFieldsTooLargeError):
        api.get('status/431')

def test_session_unavailableforlegalreasonserror(api):
    with pytest.raises(UnavailableForLegalReasonsError):
        api.get('status/451')

def test_session_servererror(api):
    with pytest.raises(ServerError):
        api.get('status/500')

def test_session_methodnotimplimentederror(api):
    with pytest.raises(MethodNotImplementedError):
        api.get('status/501')

def test_session_badgatewayerror(api):
    with pytest.raises(BadGatewayError):
        api.get('status/502')

def test_session_serviceunavailableerror(api):
    with pytest.raises(ServiceUnavailableError):
        api.get('status/503')

def test_session_gatewaytimeouterror(api):
    with pytest.raises(GatewayTimeoutError):
        api.get('status/504')

def test_session_notextendederror(api):
    with pytest.raises(NotExtendedError):
        api.get('status/510')

def test_session_networkauthrequirederror(api):
    with pytest.raises(NetworkAuthenticationRequiredError):
        api.get('status/511')
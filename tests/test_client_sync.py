# pyright: strict, reportPrivateUsage=false
import logging
import re

import pytest
from httpx import Request, Response
from pydantic import BaseModel
from pytest_httpx import HTTPXMock
from restfly import APIClient, APIError, RetryError
from restfly._sync import HTTPClientVerbs


@pytest.fixture
def client() -> APIClient:
    class TestClient(APIClient):
        _base_url: str = "https://httpbin.org"
        _lib_name: str = "RESTFlyTest"

    return TestClient(vendor="RESTFly", product="pytest")


class HTTPBinResponse(BaseModel):
    args: dict[str, object]
    headers: dict[str, str]
    origin: str
    url: str


def test_http_methods_not_implemented():
    with pytest.raises(NotImplementedError):
        HTTPClientVerbs()._request("GET", "/")


def test_request_hook(client: APIClient, caplog: pytest.LogCaptureFixture):
    req = Request(method="GET", url="https://httpbin.org")

    with caplog.at_level(logging.DEBUG):
        client._request_hook(req)

    assert "REQUESTING GET: https://httpbin.org" in caplog.text


def test_response_hook(client: APIClient, caplog: pytest.LogCaptureFixture):
    req = Request(method="GET", url="https://httpbin.org")
    resp = Response(status_code=200, request=req)

    with caplog.at_level(logging.INFO):
        client._response_hook(resp)

    assert "[200] GET: https://httpbin.org" in caplog.text


def test_hooks_in_request(
    client: APIClient, caplog: pytest.LogCaptureFixture, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(url="https://httpbin.org")

    with caplog.at_level(logging.DEBUG):
        _ = client._request("GET", "https://httpbin.org")

    assert "REQUESTING GET: https://httpbin.org" in caplog.text
    assert "[200] GET: https://httpbin.org" in caplog.text


def test_deauth_hook(httpx_mock: HTTPXMock):
    class ExClient(APIClient):
        _base_url: str = "https://httpbin.org"
        _lib_name: str = "RESTFlyTest"

        def _deauthenticate(self):
            raise TypeError("msg: Deauth")

    with pytest.raises(TypeError) as err:
        with ExClient():
            pass
    assert err.match("msg: Deauth")


def test_client_raw_request(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/get",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/get",
        },
    )
    resp = client._request("GET", "/get")
    assert isinstance(resp, Response)
    data = resp.json()
    assert data["url"] == "https://httpbin.org/get"


def test_client_retry_request(client: APIClient):
    resp = Response(
        status_code=200, request=Request(method="GET", url="https://httpbin.org")
    )
    assert resp.request == client._retry_request(resp)


def test_client_pydantic_response(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/get",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/get",
        },
    )
    resp = client._request("GET", "/get", response_model=HTTPBinResponse)
    assert isinstance(resp, HTTPBinResponse)
    assert resp.url == "https://httpbin.org/get"


def test_client_pydantic_list(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/get/list", json=[{"a": 1}, {"a": 2}]
    )

    class Test(BaseModel):
        a: int

    resp = client._request("GET", "/get/list", response_model=list[Test])
    assert resp == [Test(a=1), Test(a=2)]


def test_client_400_err(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://httpbin.org/status/400", status_code=400)
    with pytest.raises(
        APIError,
        match=re.escape("[400] Bad Request GET https://httpbin.org/status/400"),
    ):
        _ = client._request("GET", "/status/400")


def test_client_unknown_err(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://httpbin.org/status/499", status_code=499)
    with pytest.raises(
        APIError,
        match=re.escape("[499] Response from GET https://httpbin.org/status/499"),
    ):
        _ = client._request("GET", "/status/499")


def test_client_retry_err(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/status/429", status_code=429, is_reusable=True
    )
    client._error_map[429].jitter = 0
    client._error_map[429].backoff = 0
    with pytest.raises(RetryError):
        _ = client._request("GET", "/status/429")


def test_client_get_method(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/get",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/get",
        },
        is_reusable=True,
    )
    resp1 = client._get("/get")
    resp2 = client._get("/get", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/get"
    assert resp2.url == "https://httpbin.org/get"


def test_client_post_method(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/post",
        method="POST",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/post",
        },
        is_reusable=True,
    )
    resp1 = client._post("/post")
    resp2 = client._post("/post", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/post"
    assert resp2.url == "https://httpbin.org/post"


def test_client_put_method(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/put",
        method="PUT",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/put",
        },
        is_reusable=True,
    )
    resp1 = client._put("/put")
    resp2 = client._put("/put", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/put"
    assert resp2.url == "https://httpbin.org/put"


def test_client_patch_method(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/patch",
        method="PATCH",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/patch",
        },
        is_reusable=True,
    )
    resp1 = client._patch("/patch")
    resp2 = client._patch("/patch", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/patch"
    assert resp2.url == "https://httpbin.org/patch"


def test_client_delete_method(client: APIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/delete",
        method="DELETE",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/delete",
        },
        is_reusable=True,
    )
    resp1 = client._delete("/delete")
    resp2 = client._delete("/delete", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/delete"
    assert resp2.url == "https://httpbin.org/delete"

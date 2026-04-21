import re

import pytest
from httpx import Request, Response
from pydantic import BaseModel
from pytest_httpx import HTTPXMock
from restfly import APIError, AsyncAPIClient, RetryError


@pytest.fixture
def client() -> AsyncAPIClient:
    class TestClient(AsyncAPIClient):
        _base_url: str = "https://httpbin.org"
        _lib_name: str = "RESTFlyTest"

    return TestClient(vendor="RESTFly", product="pytest")


class HTTPBinResponse(BaseModel):
    args: dict[str, object]
    headers: dict[str, str]
    origin: str
    url: str


async def test_client_raw_request(client: AsyncAPIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/get",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/get",
        },
    )
    resp = await client._request("GET", "/get")
    assert isinstance(resp, Response)
    data = resp.json()
    assert data["url"] == "https://httpbin.org/get"


async def test_client_retry_request(client: AsyncAPIClient):
    resp = Response(
        status_code=200, request=Request(method="GET", url="https://httpbin.org")
    )
    assert resp.request == await client._retry_request(resp)


async def test_client_pydantic_response(client: AsyncAPIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/get",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/get",
        },
    )
    resp = await client._request("GET", "/get", response_model=HTTPBinResponse)
    assert isinstance(resp, HTTPBinResponse)
    assert resp.url == "https://httpbin.org/get"


async def test_client_pydantic_list(client: AsyncAPIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/get/list", json=[{"a": 1}, {"a": 2}]
    )

    class Test(BaseModel):
        a: int

    resp = await client._request("GET", "/get/list", response_model=list[Test])
    assert resp == [Test(a=1), Test(a=2)]


async def test_client_400_err(client: AsyncAPIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://httpbin.org/status/400", status_code=400)
    with pytest.raises(
        APIError,
        match=re.escape("[400] Bad Request GET https://httpbin.org/status/400"),
    ):
        _ = await client._request("GET", "/status/400")


async def test_client_unknown_err(client: AsyncAPIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://httpbin.org/status/499", status_code=499)
    with pytest.raises(
        APIError,
        match=re.escape("[499] Response from GET https://httpbin.org/status/499"),
    ):
        _ = await client._request("GET", "/status/499")


async def test_client_retry_err(client: AsyncAPIClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/status/429", status_code=429, is_reusable=True
    )
    client._error_map[429].jitter = 0
    client._error_map[429].backoff = 0
    with pytest.raises(RetryError):
        _ = await client._request("GET", "/status/429")


async def test_client_get_method(client: AsyncAPIClient, httpx_mock: HTTPXMock):
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
    resp1 = await client._get("/get")
    resp2 = await client._get("/get", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/get"
    assert resp2.url == "https://httpbin.org/get"


async def test_client_post_method(client: AsyncAPIClient, httpx_mock: HTTPXMock):
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
    resp1 = await client._post("/post")
    resp2 = await client._post("/post", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/post"
    assert resp2.url == "https://httpbin.org/post"


async def test_client_put_method(client: AsyncAPIClient, httpx_mock: HTTPXMock):
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
    resp1 = await client._put("/put")
    resp2 = await client._put("/put", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/put"
    assert resp2.url == "https://httpbin.org/put"


async def test_client_patch_method(client: AsyncAPIClient, httpx_mock: HTTPXMock):
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
    resp1 = await client._patch("/patch")
    resp2 = await client._patch("/patch", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/patch"
    assert resp2.url == "https://httpbin.org/patch"


async def test_client_delete_method(client: AsyncAPIClient, httpx_mock: HTTPXMock):
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
    resp1 = await client._delete("/delete")
    resp2 = await client._delete("/delete", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/delete"
    assert resp2.url == "https://httpbin.org/delete"

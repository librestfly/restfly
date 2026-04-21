import re

import pytest
from httpx import Response
from pydantic import BaseModel
from pytest_httpx import HTTPXMock
from restfly import APIError, AsyncAPIClient, AsyncAPIEndpoint, RetryError


class HTTPBinResponse(BaseModel):
    args: dict[str, object]
    headers: dict[str, str]
    origin: str
    url: str


class ExEndpoint(AsyncAPIEndpoint):
    async def get(self) -> HTTPBinResponse:
        return await self._get("/get", response_model=HTTPBinResponse)  # type: ignore


class ExPatchedEndPoint(AsyncAPIEndpoint):
    _path = "/get"

    async def get(self) -> HTTPBinResponse:
        return await self._get("", response_model=HTTPBinResponse)


class ExClient(AsyncAPIClient):
    _base_url: str = "https://httpbin.org"
    _lib_name: str = "RESTFlytTest"
    test: ExEndpoint
    tpath: ExPatchedEndPoint


@pytest.fixture
def client() -> ExClient:
    return ExClient(vendor="RESTFly", product="pytest")


async def test_endpoint_async(client: ExClient, httpx_mock: HTTPXMock):
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
    resp = await client.test.get()
    assert isinstance(resp, HTTPBinResponse)
    assert resp.url == "https://httpbin.org/get"
    resp = await client.tpath.get()
    assert isinstance(resp, HTTPBinResponse)
    assert resp.url == "https://httpbin.org/get"


async def test_endpoint_async_raw_request(client: ExClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/get",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/get",
        },
    )
    resp = await client.test._request("GET", "/get")
    assert isinstance(resp, Response)
    data = resp.json()
    assert data["url"] == "https://httpbin.org/get"


async def test_endpoint_async_pydantic_response(
    client: ExClient, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="https://httpbin.org/get",
        json={
            "args": {},
            "headers": {"Accept": "application/json"},
            "origin": "127.0.0.1",
            "url": "https://httpbin.org/get",
        },
    )
    resp = await client.test._request("GET", "/get", response_model=HTTPBinResponse)
    assert isinstance(resp, HTTPBinResponse)
    assert resp.url == "https://httpbin.org/get"


async def test_endpoint_async_pydantic_list(client: ExClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/get/list", json=[{"a": 1}, {"a": 2}]
    )

    class Test(BaseModel):
        a: int

    resp = await client.test._request("GET", "/get/list", response_model=list[Test])
    assert resp == [Test(a=1), Test(a=2)]


async def test_endpoint_async_400_err(client: ExClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://httpbin.org/status/400", status_code=400)
    with pytest.raises(
        APIError,
        match=re.escape("[400] Bad Request GET https://httpbin.org/status/400"),
    ):
        _ = await client.test._request("GET", "/status/400")


async def test_endpoint_async_unknown_err(client: ExClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://httpbin.org/status/499", status_code=499)
    with pytest.raises(
        APIError,
        match=re.escape("[499] Response from GET https://httpbin.org/status/499"),
    ):
        _ = await client.test._request("GET", "/status/499")


async def test_endpoint_async_retry_err(client: ExClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://httpbin.org/status/429", status_code=429, is_reusable=True
    )
    client._error_map[429].jitter = 0
    client._error_map[429].backoff = 0
    with pytest.raises(RetryError):
        _ = await client.test._request("GET", "/status/429")


async def test_endpoint_async_get_method(client: ExClient, httpx_mock: HTTPXMock):
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
    resp1 = await client.test._get("/get")
    resp2 = await client.test._get("/get", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/get"
    assert resp2.url == "https://httpbin.org/get"


async def test_endpoint_async_post_method(client: ExClient, httpx_mock: HTTPXMock):
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
    resp1 = await client.test._post("/post")
    resp2 = await client.test._post("/post", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/post"
    assert resp2.url == "https://httpbin.org/post"


async def test_endpoint_async_put_method(client: ExClient, httpx_mock: HTTPXMock):
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
    resp1 = await client.test._put("/put")
    resp2 = await client.test._put("/put", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/put"
    assert resp2.url == "https://httpbin.org/put"


async def test_endpoint_async_patch_method(client: ExClient, httpx_mock: HTTPXMock):
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
    resp1 = await client.test._patch("/patch")
    resp2 = await client.test._patch("/patch", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/patch"
    assert resp2.url == "https://httpbin.org/patch"


async def test_endpoint_async_delete_method(client: ExClient, httpx_mock: HTTPXMock):
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
    resp1 = await client.test._delete("/delete")
    resp2 = await client.test._delete("/delete", response_model=HTTPBinResponse)

    assert isinstance(resp1, Response)
    assert isinstance(resp2, HTTPBinResponse)
    assert resp1.json()["url"] == "https://httpbin.org/delete"
    assert resp2.url == "https://httpbin.org/delete"

import pytest
from pytest_httpx import HTTPXMock
from restfly import APIClient, APIModel, AsyncAPIClient


class ExModel(APIModel):
    __api_path__ = "/test/{model.id}"
    id: int
    name: str


class ExClient(APIClient):
    _base_url = "https://nourl.tld"


class AsyncExClient(AsyncAPIClient):
    _base_url = "https://nourl.tld"


def test_model_save(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://nourl.tld/test/123",
        method="get",
        json={"id": 123, "name": "John Smith"},
    )
    httpx_mock.add_response(
        url="https://nourl.tld/test/123",
        method="put",
        match_json={"id": 123, "name": "Updated"},
        json={"id": 123, "name": "Updated"},
    )
    httpx_mock.add_response(url="https://nourl.tld/test/123", method="delete")

    client = ExClient()
    async_client = AsyncExClient()
    mdl = client._get("/test/123", response_model=ExModel)
    mdl.name = "Updated"
    mdl.save()
    mdl.remove()

    mdl.__api_client__ = async_client
    with pytest.raises(TypeError):
        mdl.save()

    with pytest.raises(TypeError):
        mdl.remove()


async def test_async_model_save(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://nourl.tld/test/123",
        method="get",
        json={"id": 123, "name": "John Smith"},
    )
    httpx_mock.add_response(
        url="https://nourl.tld/test/123",
        method="put",
        match_json={"id": 123, "name": "Updated"},
        json={"id": 123, "name": "Updated"},
    )
    httpx_mock.add_response(url="https://nourl.tld/test/123", method="delete")

    client = ExClient()
    async_client = AsyncExClient()
    mdl = await async_client._get("/test/123", response_model=ExModel)
    mdl.name = "Updated"
    await mdl.async_save()
    await mdl.async_remove()

    mdl.__api_client__ = client
    with pytest.raises(TypeError):
        await mdl.async_save()

    with pytest.raises(TypeError):
        await mdl.async_remove()

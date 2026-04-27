import re
from typing import Any

import pytest
from httpx import Client, QueryParams
from pydantic import BaseModel
from pydantic_xml import BaseXmlModel
from restfly import APIEndpoint
from restfly._base import APIBaseEndpoint, APIClientBase


class HTTPBinResponse(BaseModel):
    args: dict[str, Any]
    headers: dict[str, str]
    origin: str
    url: str


@pytest.fixture
def client():
    class TestClient(APIClientBase):
        __client_class__ = Client
        __endpoint_class__ = APIEndpoint
        _base_url = "https://httpbin.org"
        _lib_name = "RESTFly-Test"

    return TestClient(vendor="RESTFly", product="pytest")


def test_client_init(client: APIClientBase):
    rua = re.compile(
        (
            r"Integration/1\.0 \([\w\d\-\ ]+;[\w\d\-\ ]+; Build/[\w\d\.\-\ ]+\) "
            r"[\w\d\-]+/[\w\d\.\-]+ "
            r"\(RESTFly/[\w\d\.\-]+; HTTPX/[\w\d\-\.]+; Python/[0-9\.\-]+; [\w\d\-]+/[\d\w\-]+\)"
        )
    )

    assert client._base_url == "https://httpbin.org"
    assert isinstance(client._client, Client)

    sync_user_agent = client._client.headers.get("user-agent")

    assert rua.match(sync_user_agent) is not None


def test_client_init_url_overload():
    class TestClient(APIClientBase):
        __client_class__ = Client
        __endpoint_class__ = APIEndpoint
        _base_url = "https://test.com"

    client = TestClient(base_url="https://httpbin.org")
    assert client._base_url == "https://httpbin.org"


def test_client_marshal_pydantic_params(client: APIClientBase):
    class Test(BaseModel):
        a: int

    x = Test(a=1)
    y = Test(a=42)

    resp = client._request_pre_process(method="GET", url="", params=x, json=y)
    assert resp["params"] == {"a": 1}
    assert resp["content"] == '{"a":42}'
    assert resp["headers"] == {"Content-Type": "application/json"}


def test_client_marshal_xml_params(client: APIClientBase):
    class Test(BaseXmlModel):
        a: int

    resp = client._request_pre_process(
        method="GET", url="", params=Test(a=1), xml=Test(a=42)
    )
    assert resp["params"] == {"a": 1}
    assert resp["content"] == b"<Test>42</Test>"
    assert resp["headers"] == {"Content-Type": "application/xml"}


def test_client_marshal_json_dict_passthrough(client: APIClientBase):
    resp = client._request_pre_process(method="GET", url="", json={"a": 1})
    assert resp["json"] == {"a": 1}


def test_client_marshal_xml_string_passthrough(client: APIClientBase):
    resp = client._request_pre_process(method="GET", url="", xml="<Test>1</Test>")
    assert resp["content"] == "<Test>1</Test>"
    assert resp["headers"] == {"Content-Type": "application/xml"}


def test_client_basemodel_queryparams():
    class ExampleParams(BaseModel):
        test: int

    class TestClient(APIClientBase):
        __client_class__ = Client
        __endpoint_class__ = APIEndpoint
        _base_url = "https://httpbin.org"
        _lib_name = "RESTFly-Test"

    params = ExampleParams(test=1)
    client = TestClient(params=params)
    assert client._client._params == QueryParams("test=1")


def test_base_endpoint_init():
    class OkCode(APIBaseEndpoint):
        _path = "/200"

    class CodesAPI(APIBaseEndpoint):
        _path = "/status"

        ok: OkCode

    class TestClient(APIClientBase):
        __client_class__ = Client
        __endpoint_class__ = APIBaseEndpoint
        _base_url = "https://httpbin.org"
        _lib_name = "RESTFly-Test"

        codes: CodesAPI

    client = TestClient()
    assert client == client.codes._client == client.codes.ok._client


def test_base_endpoint_typerror_init():
    class Failpoint(APIBaseEndpoint):
        _path = "/status"

    with pytest.raises(TypeError) as err:
        _ = Failpoint(None)  # ty: ignore[invalid-argument-type]

    assert err.match(r"Client \w+ is not a valid client type.")

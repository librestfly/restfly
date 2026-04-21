import pytest
from httpbin.client import HTTPBinClient
from httpbin.models import HTTPBinResponse, Slideshow, XmlSlideshow
from pytest_httpx import HTTPXMock
from restfly import APIError

ex_resp = {
    "args": {},
    "headers": {"Accept": "application/json"},
    "origin": "127.0.0.1",
    "url": "https://httpbin.org/get",
}


def test_httpbin_client_init(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://httpbin.org/get", json=ex_resp)
    client = HTTPBinClient()
    data = client._get("/get").json()
    assert data["origin"] == "127.0.0.1"


def test_httpbin_client_methods(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://httpbin.org/get", method="get", json=ex_resp)
    httpx_mock.add_response(url="https://httpbin.org/post", method="post", json=ex_resp)
    httpx_mock.add_response(url="https://httpbin.org/put", method="put", json=ex_resp)
    httpx_mock.add_response(
        url="https://httpbin.org/patch", method="patch", json=ex_resp
    )
    httpx_mock.add_response(
        url="https://httpbin.org/delete", method="delete", json=ex_resp
    )

    client = HTTPBinClient()
    test_resp = HTTPBinResponse.model_validate(ex_resp)
    assert client.methods.get() == test_resp
    assert client.methods.post() == test_resp
    assert client.methods.put() == test_resp
    assert client.methods.patch() == test_resp
    assert client.methods.delete() == test_resp


def test_httpbin_client_status_codes(httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="get", url="https://httpbin.org/status/200")
    httpx_mock.add_response(method="post", url="https://httpbin.org/status/200")
    httpx_mock.add_response(method="patch", url="https://httpbin.org/status/200")
    httpx_mock.add_response(method="put", url="https://httpbin.org/status/200")
    httpx_mock.add_response(method="delete", url="https://httpbin.org/status/200")
    httpx_mock.add_response(
        status_code=400, method="get", url="https://httpbin.org/status/400"
    )

    client = HTTPBinClient()
    assert client.codes.get(200).status_code == 200
    assert client.codes.post(200).status_code == 200
    assert client.codes.patch(200).status_code == 200
    assert client.codes.put(200).status_code == 200
    assert client.codes.delete(200).status_code == 200

    with pytest.raises(APIError):
        client.codes.get(400)


def test_httpbin_client_json_response(httpx_mock: HTTPXMock):
    payload = {
        "slideshow": {
            "author": "Yours Truly",
            "date": "date of publication",
            "slides": [
                {"title": "Wake up to WonderWidgets!", "type": "all"},
                {
                    "items": [
                        "Why <em>WonderWidgets</em> are great",
                        "Who <em>buys</em> WonderWidgets",
                    ],
                    "title": "Overview",
                    "type": "all",
                },
            ],
            "title": "Sample Slide Show",
        }
    }
    test_resp = Slideshow.model_validate(payload["slideshow"])
    httpx_mock.add_response(url="https://httpbin.org/json", json=payload)
    client = HTTPBinClient()
    assert client.formats.json() == test_resp


def test_httpbin_client_xml_response(httpx_mock: HTTPXMock):
    payload = b"""<?xml version='1.0' encoding='us-ascii'?>
      <!--  A SAMPLE set of slides  -->
      <slideshow
        title="Sample Slide Show"
        date="Date of publication"
        author="Yours Truly"
        >
        <!-- TITLE SLIDE -->
        <slide type="all">
          <title>Wake up to WonderWidgets!</title>
        </slide>
        <!-- OVERVIEW -->
        <slide type="all">
          <title>Overview</title>
          <item>
            Why
            <em>WonderWidgets</em>
             are great
          </item>
          <item/>
          <item>
            Who
            <em>buys</em>
             WonderWidgets
          </item>
        </slide>
      </slideshow>
    """
    test_resp = XmlSlideshow.from_xml(payload)
    httpx_mock.add_response(url="https://httpbin.org/xml", content=payload)
    client = HTTPBinClient()
    assert client.formats.xml() == test_resp

from __future__ import annotations

from httpx import Response
from restfly import APIClient, APIEndpoint

from . import models


class HTTPBinClient(APIClient):
    _base_url = "https://httpbin.org"

    methods: MethodsAPI
    codes: StatusCodesAPI
    formats: ResponseFormatsAPI


class MethodsAPI(APIEndpoint):
    def get(self) -> models.HTTPBinResponse:
        return self._get("/get", response_model=models.HTTPBinResponse)

    def post(self) -> models.HTTPBinResponse:
        return self._post("/post", response_model=models.HTTPBinResponse)

    def put(self) -> models.HTTPBinResponse:
        return self._put("/put", response_model=models.HTTPBinResponse)

    def patch(self) -> models.HTTPBinResponse:
        return self._patch("/patch", response_model=models.HTTPBinResponse)

    def delete(self) -> models.HTTPBinResponse:
        return self._delete("/delete", response_model=models.HTTPBinResponse)


class StatusCodesAPI(APIEndpoint):
    _path = "/status"

    def get(self, status_code: int) -> Response:
        return self._get(f"/{status_code}")

    def post(self, status_code: int) -> Response:
        return self._post(f"/{status_code}")

    def put(self, status_code: int) -> Response:
        return self._put(f"/{status_code}")

    def patch(self, status_code: int) -> Response:
        return self._patch(f"/{status_code}")

    def delete(self, status_code: int) -> Response:
        return self._delete(f"/{status_code}")


class ResponseFormatsAPI(APIEndpoint):
    def json(self) -> models.Slideshow:
        resp = self._get("/json", response_model=models.JsonResponse)
        return resp.slideshow

    def xml(self) -> models.XmlSlideshow:
        return self._get("/xml", response_model=models.XmlSlideshow)

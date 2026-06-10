from typing import Literal, TypeVar

from httpx import (
    AsyncBaseTransport,
    AsyncClient,
    BaseTransport,
    Client,
    Request,
    Response,
    codes,
)
from httpx import __version__ as HTTPX_VERSION
from httpx._client import USE_CLIENT_DEFAULT, BaseClient, EventHook, UseClientDefault
from httpx._config import (
    DEFAULT_LIMITS,
    DEFAULT_MAX_REDIRECTS,
    DEFAULT_TIMEOUT_CONFIG,
    Limits,
)
from httpx._types import (
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxyTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    TimeoutTypes,
)
from httpx._types import (
    QueryParamTypes as _QueryParamTypes,
)
from httpx._urls import URL
from pydantic import BaseModel
from pydantic_xml import BaseXmlModel

Model = TypeVar("Model", bound=BaseModel)
XMLModel = TypeVar("XMLModel", bound=BaseXmlModel)

HTTPMethods = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
QueryParamTypes = BaseModel | _QueryParamTypes

__all__ = [
    "DEFAULT_LIMITS",
    "DEFAULT_MAX_REDIRECTS",
    "DEFAULT_TIMEOUT_CONFIG",
    "HTTPX_VERSION",
    "URL",
    "USE_CLIENT_DEFAULT",
    "AsyncBaseTransport",
    "AsyncClient",
    "AuthTypes",
    "BaseClient",
    "BaseTransport",
    "CertTypes",
    "Client",
    "CookieTypes",
    "EventHook",
    "HeaderTypes",
    "HTTPMethods",
    "Limits",
    "Model",
    "ProxyTypes",
    "QueryParamTypes",
    "Request",
    "RequestContent",
    "RequestData",
    "RequestExtensions",
    "RequestFiles",
    "Response",
    "UseClientDefault",
    "TimeoutTypes",
    "XMLModel",
    "codes",
]

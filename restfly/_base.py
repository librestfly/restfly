from __future__ import annotations

import logging
import platform
from collections import defaultdict
from ssl import SSLContext
from typing import Any, Callable

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel

from ._errors import ERROR_MAP, ErrorStatus, default_error_status
from ._types import (
    DEFAULT_LIMITS,
    DEFAULT_MAX_REDIRECTS,
    DEFAULT_TIMEOUT_CONFIG,
    HTTPX_VERSION,
    USE_CLIENT_DEFAULT,
    AsyncBaseTransport,
    AsyncClient,
    AuthTypes,
    BaseTransport,
    CertTypes,
    Client,
    CookieTypes,
    EventHook,
    HeaderTypes,
    HTTPMethods,
    Limits,
    Model,
    ProxyTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    TimeoutTypes,
    UseClientDefault,
    XMLModel,
)
from ._utils import assign_annotations
from ._version import version as RESTFLY_VERSION


class APIClientBase:
    __client_class__: type[Client] | type[AsyncClient]
    __endpoint_class__: type[APIBaseEndpoint]

    _base_url: str = ""
    """ The base URL fragment to prefix all API calls with. """

    _client: Client | AsyncClient
    """ HTTPX Client Session object """

    _json_model_kwargs: dict[str, Any]
    """ Client-level Pydantic BaseModel.model_dump kwargs """

    _xml_model_kwargs: dict[str, Any]
    """ Client-level Pydantic-XML BaseXmlModel.to_xml kwargs """

    _lib_name: str = "RESTFly"
    """ Library name """

    _lib_version: str = "2"
    """ Library version """

    _retry_max: int = 5
    """ Maximum number of retries to attempt before giving up. """

    _logger: logging.Logger
    """ Logger for the client """

    __error_map__: dict[int, ErrorStatus] = ERROR_MAP
    """ The default error map """

    _error_map: defaultdict[int, ErrorStatus]
    """
    The error map determining how to handle non-OK status codes. Represented by the
    integer status code along with an ErrorStatus data-class object detailing how to
    handle the response. Any overloads to the base error map should be provided here
    and this attribute will be then be replaced at initialization with the merging of
    the default map, this attribute, and anything passed to the constructor. The
    resulting error map will be used during operation of the APIClass object.
    """

    def __init__(
        self,
        *,
        auth: AuthTypes | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        verify: SSLContext | str | bool = True,
        cert: CertTypes | None = None,
        http1: bool = True,
        http2: bool = False,
        proxy: ProxyTypes | None = None,
        mounts: (dict[str, Any]) | None = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        follow_redirects: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: (dict[str, list[EventHook]]) | None = None,
        base_url: str | None = None,
        transport: AsyncBaseTransport | BaseTransport | None = None,
        trust_env: bool = True,
        default_encoding: str | Callable[[bytes], str] = "utf-8",
        vendor: str = "unknown",
        product: str = "unknown",
        build: str = "unknown",
        retry_max: int = 5,
        json_model_kwargs: dict[str, Any] | None = None,
        xml_model_kwargs: dict[str, Any] | None = None,
        error_map: dict[int, ErrorStatus] | None = None,
    ) -> None:
        # Initialize mutables.
        headers = {} if headers is None else headers
        error_map = {} if error_map is None else error_map

        # Initialize the private attributes for the client object.
        self._base_url = base_url if base_url else self._base_url
        self._logger = logging.getLogger(__name__)
        self._retry_max = retry_max if retry_max else self._retry_max
        self._json_model_kwargs = json_model_kwargs if json_model_kwargs else {}
        self._xml_model_kwargs = xml_model_kwargs if xml_model_kwargs else {}

        # Construct the Error Map default dict using the built-in error_map as well as
        # the over loadable _error_map extension and then lastly update with any
        # error_map provided at initialization.  Lastly store the resulting defaultdict
        # over the _error_map private attribute.
        emap = defaultdict(default_error_status, self.__error_map__)
        for updates in (getattr(self, "_error_map", {}), error_map):
            emap.update(updates)
        self._error_map = emap

        # If we had received a pydantic model for the client params, then we will first
        # coerce them into a python dictionary.
        if isinstance(params, BaseModel):
            params = params.model_dump(mode="json", exclude_none=True)

        # Instantiate the HTTPX Client with the arguments we have.
        self._client = self.__client_class__(
            auth=auth,
            params=params,
            headers=headers,
            cookies=cookies,
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            proxy=proxy,
            mounts=mounts,
            timeout=timeout,
            follow_redirects=follow_redirects,
            limits=limits,
            max_redirects=max_redirects,
            event_hooks=event_hooks,
            base_url=self._base_url,
            transport=transport,  # type: ignore[arg-type]
            trust_env=trust_env,
            default_encoding=default_encoding,
        )

        # Update the client with the User-Agent header.
        user_agent = (
            f"Integration/1.0 ({vendor}; {product}; Build/{build}) "
            f"{self._lib_name}/{self._lib_version} "
            f"(RESTFly/{RESTFLY_VERSION}; "
            f"HTTPX/{self.__client_class__.__name__}-{HTTPX_VERSION}; "
            f"Python/{platform.python_version()}; "
            f"{platform.system()}/{platform.machine()})"
        )
        self._client.headers.update({"User-Agent": user_agent})

        # Lastly, we will run the annotation assignment build-in to make sure that the
        # public endpoints are properly grafted to the client class.
        self.__assign_annotations__()

    def _request_pre_process(
        self,
        method: HTTPMethods,
        url: str,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Model | object | None = None,
        xml: XMLModel | str | bytes | None = None,
        headers: dict[str, str] | None = None,
        request_model_kwargs: dict[str, Any] | None = None,
        cookies: CookieTypes | None = None,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ) -> dict[str, Any]:
        """
        Performs preflight pre-processing of the request in preparation to be sent to
        HTTPX. Most notably this method is what handles any potential model marshalling
        into the request format.  The output is passed as the kwargs into HTTPXs
        request builder.

        Args:
            method: The HTTP Method.
            url: The HTTP url (this can be either a partial or a full URL).
            params: Query parameters.
            content: Raw request content.
            data: The HTTP request body.
            files: Any files to upload with the request.
            json: Overrides the content and data attributes with JSON-formatted data.
            xml: Overrides the content and data attributes with XML-formatted data.
            headers: Any additional headers to pass into the request.
            request_model_kwargs:
                The pydantic/pydantic-xml kwargs to be passed to the model as part of
                marshalling the data into the expected format.
            cookies: The cookies to pass to the request.
            timeout: The HTTP request timeout.
            extensions: Any request extensions passed as part of the request.

        Returns:
            The kwargs dictionary to be passed to the request builder.
        """
        # Initialize mutables
        headers = {} if headers is None else headers
        request_model_kwargs = (
            {} if request_model_kwargs is None else request_model_kwargs
        )

        # The query parameters must always be transformed into a dictionary to be
        # properly passed to HTTPX
        if isinstance(params, BaseModel):
            params = params.model_dump(mode="json", **self._json_model_kwargs)

        # If the XML model actually is Pydantic-XML model, then we will want to marshal
        # it into bytes and set the content type to XML.
        if isinstance(xml, BaseXmlModel):
            xml_kwargs: dict[str, Any] = {}
            for updates in (
                getattr(self, "_xml_model_kwargs", {}),
                request_model_kwargs,
            ):
                xml_kwargs.update(updates)
            content = xml.to_xml(**xml_kwargs)
            headers["Content-Type"] = "application/xml"

        # If the xml attribute is already a string or bytes object, then simply set
        # the content type to XML.
        elif isinstance(xml, (str, bytes)):
            content = xml
            headers["Content-Type"] = "application/xml"

        # If the json attribute is actually a Pydantic model, then we will want to
        # marshal the data using Pydantics model dump and set the content type to JSON
        elif isinstance(json, BaseModel):
            pydantic_kwargs: dict[str, Any] = {}
            for updates in (
                getattr(self, "_json_model_kwargs", {}),
                request_model_kwargs,
            ):
                pydantic_kwargs.update(updates)
            content = json.model_dump_json(**pydantic_kwargs)
            headers["Content-Type"] = "application/json"
            json = None

        # Return the kwargs to the caller.
        return {
            "method": method,
            "url": url,
            "params": params,
            "content": content,
            "data": data,
            "files": files,
            "json": json,
            "headers": headers,
            "cookies": cookies,
            "timeout": timeout,
            "extensions": extensions,
        }

    def __assign_annotations__(self) -> None:
        """
        Handles Annotation assignment for API Endpoints.
        """
        assign_annotations(self, self.__endpoint_class__)


class APIBaseEndpoint:
    _path: str | None = None
    """ Path fragment to append to the base url already stored within the client. """

    _logger: logging.Logger
    """
    The same logging handler that the client has, it also exists here for convenience.
    """

    _client: APIClientBase
    """
    The client object that this endpoint is associated with. Provided here in order to
    interact with other endpoints that may be grafted to the client.
    """

    def __init__(self, client: APIClientBase | APIBaseEndpoint) -> None:
        match client:
            case APIClientBase():
                self._client = client
            case APIBaseEndpoint():
                self._client = client._client
            case _:
                raise TypeError(f"Client {client} is not a valid client type.")
        self._logger = client._logger
        assign_annotations(self, self._client.__endpoint_class__)

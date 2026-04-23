from __future__ import annotations

import random
from ssl import SSLContext
from time import sleep
from typing import Any, Callable, Literal, Self, overload, override

from ._base import APIBaseEndpoint, APIClientBase
from ._errors import ErrorStatus, RetryError
from ._types import (
    DEFAULT_LIMITS,
    DEFAULT_MAX_REDIRECTS,
    DEFAULT_TIMEOUT_CONFIG,
    USE_CLIENT_DEFAULT,
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
    Request,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    Response,
    TimeoutTypes,
    UseClientDefault,
    XMLModel,
    codes,
)
from ._utils import assign_annotations, unmarshal


class HTTPClientVerbs:
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        response_model: type[Model] | type[list[Model]] | None = None,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        headers: dict[str, str] | None = None,
        json: Model | Any | None = None,
        xml: XMLModel | str | bytes | None = None,
        response_model_kwargs: dict[str, Any] | None = None,
        request_model_kwargs: dict[str, Any] | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        max_retries: int | None = None,
        error_map: dict[int, ErrorStatus] | None = None,
    ) -> Model | list[Model] | Response:
        raise NotImplementedError

    @overload
    def _get(
        self,
        path: str,
        *,
        response_model: None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        params: QueryParamTypes | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Response: ...

    @overload
    def _get(
        self,
        path: str,
        *,
        response_model: type[Model],
        response_model_kwargs: dict[str, Any] | None = ...,
        params: QueryParamTypes | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Model: ...

    @overload
    def _get(
        self,
        path: str,
        *,
        response_model: type[list[Model]],
        response_model_kwargs: dict[str, Any] | None = ...,
        params: QueryParamTypes | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> list[Model]: ...

    def _get(
        self,
        path: str,
        *,
        response_model: type[Model] | type[list[Model]] | None = None,
        response_model_kwargs: dict[str, Any] | None = None,
        params: QueryParamTypes | None = None,
        headers: dict[str, str] | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        max_retries: int | None = None,
        error_map: dict[int, ErrorStatus] | None = None,
    ) -> Model | list[Model] | Response:
        """
        Construct and send an HTTP GET request.

        Args:
            path:
                URL to query.
            response_model:
                Pydantic model to coerce the response into.
            response_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                un-marshalling the response data.
            params:
                Request query parameters.
            headers:
                Request-specific headers.
            cookies:
                Request-specific cookies.
            auth:
                Request-specific authentication.
            follow_redirects:
                Should the client follow any redirects?
            timeout:
                Request-specific timeout settings.
            extensions:
                Any additional httpx extensions to pass to the client.
            max_retries:
                The maximum number of retries to attempt before giving up. Overloads
                the client default.
            error_map:
                Replaces the client error map with this one instead.

        Returns:
            Returns the HTTPX Response object if no response_model is specified. If a
            response_model _is_ specified, then the response will be coerced into the
            response model and the instance of the model will be returned.
        """
        return self._request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            response_model=response_model,
            response_model_kwargs=response_model_kwargs,
            max_retries=max_retries,
            error_map=error_map,
        )

    @overload
    def _post(
        self,
        path: str,
        *,
        response_model: Literal[None] = ...,
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Response: ...

    @overload
    def _post(
        self,
        path: str,
        *,
        response_model: type[Model],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Model: ...

    @overload
    def _post(
        self,
        path: str,
        *,
        response_model: type[list[Model]],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> list[Model]: ...

    def _post(
        self,
        path: str,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Model | Any | None = None,
        xml: XMLModel | str | bytes | None = None,
        headers: dict[str, str] | None = None,
        response_model: type[Model] | type[list[Model]] | None = None,
        response_model_kwargs: dict[str, Any] | None = None,
        request_model_kwargs: dict[str, Any] | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        max_retries: int | None = None,
        error_map: dict[int, ErrorStatus] | None = None,
    ) -> Model | list[Model] | Response:
        """
        Construct and send an HTTP POST request.

        Args:
            path:
                URL to query.
            response_model:
                Pydantic model to coerce the response into.
            response_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                un-marshalling the response data.
            request_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                marshalling the body of the data into the request.
            params:
                Request query parameters.
            content:
                Raw body of the request.
            data:
                URL form-encoded body for the request.
            json:
                Data object to marshal into JSON. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            xml:
                Data object to marshal into XML. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            files:
                A dictionary of upload files to include in the body of the request.
            headers:
                Request-specific headers.
            cookies:
                Request-specific cookies.
            auth:
                Request-specific authentication.
            follow_redirects:
                Should the client follow any redirects?
            timeout:
                Request-specific timeout settings.
            extensions:
                Any additional httpx extensions to pass to the client.
            max_retries:
                The maximum number of retries to attempt before giving up. Overloads
                the client default.
            error_map:
                Replaces the client error map with this one instead.

        Returns:
            Returns the HTTPX Response object if no response_model is specified. If a
            response_model _is_ specified, then the response will be coerced into the
            response model and the instance of the model will be returned.
        """
        return self._request(
            method="POST",
            path=path,
            params=params,
            content=content,
            data=data,
            files=files,
            json=json,
            xml=xml,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            response_model=response_model,
            response_model_kwargs=response_model_kwargs,
            request_model_kwargs=request_model_kwargs,
            max_retries=max_retries,
            error_map=error_map,
        )

    @overload
    def _put(
        self,
        path: str,
        *,
        response_model: Literal[None] = ...,
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Response: ...

    @overload
    def _put(
        self,
        path: str,
        *,
        response_model: type[Model],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Model: ...

    @overload
    def _put(
        self,
        path: str,
        *,
        response_model: type[list[Model]],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> list[Model]: ...

    def _put(
        self,
        path: str,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Model | Any | None = None,
        xml: XMLModel | str | bytes | None = None,
        headers: dict[str, str] | None = None,
        response_model: type[Model] | type[list[Model]] | None = None,
        response_model_kwargs: dict[str, Any] | None = None,
        request_model_kwargs: dict[str, Any] | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        max_retries: int | None = None,
        error_map: dict[int, ErrorStatus] | None = None,
    ) -> Model | list[Model] | Response:
        """
        Construct and send an HTTP PUT request.

        Args:
            path:
                URL to query.
            response_model:
                Pydantic model to coerce the response into.
            response_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                un-marshalling the response data.
            request_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                marshalling the body of the data into the request.
            params:
                Request query parameters.
            content:
                Raw body of the request.
            data:
                URL form-encoded body for the request.
            json:
                Data object to marshal into JSON. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            xml:
                Data object to marshal into XML. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            files:
                A dictionary of upload files to include in the body of the request.
            headers:
                Request-specific headers.
            cookies:
                Request-specific cookies.
            auth:
                Request-specific authentication.
            follow_redirects:
                Should the client follow any redirects?
            timeout:
                Request-specific timeout settings.
            extensions:
                Any additional httpx extensions to pass to the client.
            max_retries:
                The maximum number of retries to attempt before giving up. Overloads
                the client default.
            error_map:
                Replaces the client error map with this one instead.

        Returns:
            Returns the HTTPX Response object if no response_model is specified. If a
            response_model _is_ specified, then the response will be coerced into the
            response model and the instance of the model will be returned.
        """
        return self._request(
            method="PUT",
            path=path,
            params=params,
            content=content,
            data=data,
            files=files,
            json=json,
            xml=xml,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            response_model=response_model,
            response_model_kwargs=response_model_kwargs,
            request_model_kwargs=request_model_kwargs,
            max_retries=max_retries,
            error_map=error_map,
        )

    @overload
    def _patch(
        self,
        path: str,
        *,
        response_model: Literal[None] = ...,
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Response: ...

    @overload
    def _patch(
        self,
        path: str,
        *,
        response_model: type[Model],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Model: ...

    @overload
    def _patch(
        self,
        path: str,
        *,
        response_model: type[list[Model]],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> list[Model]: ...

    def _patch(
        self,
        path: str,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Model | Any | None = None,
        xml: XMLModel | str | bytes | None = None,
        headers: dict[str, str] | None = None,
        response_model: type[Model] | type[list[Model]] | None = None,
        response_model_kwargs: dict[str, Any] | None = None,
        request_model_kwargs: dict[str, Any] | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        max_retries: int | None = None,
        error_map: dict[int, ErrorStatus] | None = None,
    ) -> Model | list[Model] | Response:
        """
        Construct and send an HTTP PATCH request.

        Args:
            path:
                URL to query.
            response_model:
                Pydantic model to coerce the response into.
            response_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                un-marshalling the response data.
            request_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                marshalling the body of the data into the request.
            params:
                Request query parameters.
            content:
                Raw body of the request.
            data:
                URL form-encoded body for the request.
            json:
                Data object to marshal into JSON. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            xml:
                Data object to marshal into XML. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            files:
                A dictionary of upload files to include in the body of the request.
            headers:
                Request-specific headers.
            cookies:
                Request-specific cookies.
            auth:
                Request-specific authentication.
            follow_redirects:
                Should the client follow any redirects?
            timeout:
                Request-specific timeout settings.
            extensions:
                Any additional httpx extensions to pass to the client.
            max_retries:
                The maximum number of retries to attempt before giving up. Overloads
                the client default.
            error_map:
                Replaces the client error map with this one instead.

        Returns:
            Returns the HTTPX Response object if no response_model is specified. If a
            response_model _is_ specified, then the response will be coerced into the
            response model and the instance of the model will be returned.
        """
        return self._request(
            method="PATCH",
            path=path,
            params=params,
            content=content,
            data=data,
            files=files,
            json=json,
            xml=xml,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            response_model=response_model,
            response_model_kwargs=response_model_kwargs,
            request_model_kwargs=request_model_kwargs,
            max_retries=max_retries,
            error_map=error_map,
        )

    @overload
    def _delete(
        self,
        path: str,
        *,
        response_model: Literal[None] = ...,
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Response: ...

    @overload
    def _delete(
        self,
        path: str,
        *,
        response_model: type[Model],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Model: ...

    @overload
    def _delete(
        self,
        path: str,
        *,
        response_model: type[list[Model]],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> list[Model]: ...

    def _delete(
        self,
        path: str,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Model | Any | None = None,
        xml: XMLModel | str | bytes | None = None,
        headers: dict[str, str] | None = None,
        response_model: type[Model] | type[list[Model]] | None = None,
        response_model_kwargs: dict[str, Any] | None = None,
        request_model_kwargs: dict[str, Any] | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        max_retries: int | None = None,
        error_map: dict[int, ErrorStatus] | None = None,
    ) -> Model | list[Model] | Response:
        """
        Construct and send an HTTP DELETE request.

        Args:
            path:
                URL to query.
            response_model:
                Pydantic model to coerce the response into.
            response_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                un-marshalling the response data.
            request_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                marshalling the body of the data into the request.
            params:
                Request query parameters.
            content:
                Raw body of the request.
            data:
                URL form-encoded body for the request.
            json:
                Data object to marshal into JSON. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            xml:
                Data object to marshal into XML. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            files:
                A dictionary of upload files to include in the body of the request.
            headers:
                Request-specific headers.
            cookies:
                Request-specific cookies.
            auth:
                Request-specific authentication.
            follow_redirects:
                Should the client follow any redirects?
            timeout:
                Request-specific timeout settings.
            extensions:
                Any additional httpx extensions to pass to the client.
            max_retries:
                The maximum number of retries to attempt before giving up. Overloads
                the client default.
            error_map:
                Replaces the client error map with this one instead.

        Returns:
            Returns the HTTPX Response object if no response_model is specified. If a
            response_model _is_ specified, then the response will be coerced into the
            response model and the instance of the model will be returned.
        """
        return self._request(
            method="DELETE",
            path=path,
            params=params,
            content=content,
            data=data,
            files=files,
            json=json,
            xml=xml,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            response_model=response_model,
            response_model_kwargs=response_model_kwargs,
            request_model_kwargs=request_model_kwargs,
            max_retries=max_retries,
            error_map=error_map,
        )


class APIEndpoint(APIBaseEndpoint, HTTPClientVerbs):
    _client: APIClient

    def __init__(self, client: APIClient | APIEndpoint) -> None:
        super().__init__(client)

    @overload
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        response_model: Literal[None] = ...,
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Response: ...

    @overload
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        response_model: type[Model],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Model: ...

    @overload
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        response_model: type[list[Model]],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> list[Model]: ...

    @overload
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        response_model: type[Model] | type[list[Model]] | None = ...,
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Model | list[Model] | Response: ...

    @override
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        headers: dict[str, str] | None = None,
        json: Model | Any | None = None,
        xml: XMLModel | str | bytes | None = None,
        response_model: type[Model] | type[list[Model]] | None = None,
        response_model_kwargs: dict[str, Any] | None = None,
        request_model_kwargs: dict[str, Any] | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        max_retries: int | None = None,
        error_map: dict[int, ErrorStatus] | None = None,
    ) -> Model | list[Model] | Response:
        """
        Construct and send an HTTP POST request.

        Args:
            method:
                The HTTP method used for the request.
            path:
                URL to query.
            response_model:
                Pydantic model to coerce the response into.
            response_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                un-marshalling the response data.
            request_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                marshalling the body of the data into the request.
            params:
                Request query parameters.
            content:
                Raw body of the request.
            data:
                URL form-encoded body for the request.
            json:
                Data object to marshal into JSON. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            xml:
                Data object to marshal into XML. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            files:
                A dictionary of upload files to include in the body of the request.
            headers:
                Request-specific headers.
            cookies:
                Request-specific cookies.
            auth:
                Request-specific authentication.
            follow_redirects:
                Should the client follow any redirects?
            timeout:
                Request-specific timeout settings.
            extensions:
                Any additional httpx extensions to pass to the client.
            max_retries:
                The maximum number of retries to attempt before giving up. Overloads
                the client default.
            error_map:
                Replaces the client error map with this one instead.

        Returns:
            Returns the HTTPX Response object if no response_model is specified. If a
            response_model _is_ specified, then the response will be coerced into the
            response model and the instance of the model will be returned.
        """
        if self._path is not None:
            path = f"{self._path}{path}"

        return self._client._request(
            method=method,
            path=path,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            json=json,
            xml=xml,
            content=content,
            data=data,
            files=files,
            response_model=response_model,
            max_retries=max_retries,
            response_model_kwargs=response_model_kwargs,
            request_model_kwargs=request_model_kwargs,
            error_map=error_map,
        )


class APIClient(APIClientBase, HTTPClientVerbs):
    __client_class__: type[Client] = Client
    __endpoint_class__: type[APIEndpoint] = APIEndpoint
    _client: Client

    @override
    def __assign_annotations__(self) -> None:
        """
        Any public annotations that are a subclass of the APIEndpoint class will be
        assigned at initialization of the object through this method.
        """
        assign_annotations(self, APIEndpoint)

    def __enter__(self) -> Self:
        """
        Context Manager __enter__ dunder. See PEP-343 for more details.
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Context Manager __exit__ dunder. See PEP-343 for more details.
        """
        return self._deauthenticate()

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
        mounts: (dict[str, BaseTransport | None]) | None = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        follow_redirects: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: (dict[str, list[EventHook]]) | None = None,
        base_url: str | None = None,
        transport: BaseTransport | None = None,
        trust_env: bool = True,
        default_encoding: str | Callable[[bytes], str] = "utf-8",
        vendor: str = "unknown",
        product: str = "unknown",
        build: str = "unknown",
        retry_max: int = 5,
    ) -> None:
        # Add the class event hooks to loop in the logging facilities.
        event_hooks = {} if event_hooks is None else event_hooks
        event_hooks = {
            "request": [self._request_hook] + list(event_hooks.get("request", [])),
            "response": [self._response_hook] + list(event_hooks.get("response", [])),
        }
        super().__init__(
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
            base_url=base_url,
            transport=transport,
            trust_env=trust_env,
            default_encoding=default_encoding,
            vendor=vendor,
            product=product,
            build=build,
            retry_max=retry_max,
        )

    def _deauthenticate(self):
        """
        De-authentication stub.  De-authentication is automatically run as part
        of leaving context within the context manager.

        Example:
            >>> class ExampleAPISession(APISession):
            ...     def _deauthenticate(self):
            ...         self.delete('session/token')
        """

    def _request_hook(self, request: Request) -> None:
        """
        The Request hook used for debug logging.

        Args:
            request: The request object.
        """
        self._logger.debug(f"REQUESTING {request.method}: {request.url}")

    def _response_hook(self, response: Response) -> None:
        """
        The Response hook used for informational logging.

        Args:
            response: The response object.
        """
        self._logger.info(
            f"[{response.status_code}] {response.request.method}: {response.request.url}"
        )

    def _retry_request(self, response: Response) -> Request:
        """
        Processes the request from the response for the purpose of retrying it again.

        Args:
            response: The response object
        """
        return response.request

    @overload
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        response_model: Literal[None] = ...,
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Response: ...

    @overload
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        response_model: type[Model],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Model: ...

    @overload
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        response_model: type[list[Model]],
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> list[Model]: ...

    @overload
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        response_model: type[Model] | type[list[Model]] | None = ...,
        params: QueryParamTypes | None = ...,
        content: RequestContent | None = ...,
        data: RequestData | None = ...,
        files: RequestFiles | None = ...,
        json: Model | Any | None = ...,
        xml: XMLModel | str | bytes | None = ...,
        response_model_kwargs: dict[str, Any] | None = ...,
        request_model_kwargs: dict[str, Any] | None = ...,
        headers: dict[str, str] | None = ...,
        cookies: CookieTypes | None = ...,
        auth: AuthTypes | UseClientDefault | None = ...,
        follow_redirects: bool | UseClientDefault = ...,
        timeout: TimeoutTypes | UseClientDefault = ...,
        extensions: RequestExtensions | None = ...,
        max_retries: int | None = ...,
        error_map: dict[int, ErrorStatus] | None = ...,
    ) -> Model | list[Model] | Response: ...

    @override
    def _request(
        self,
        method: HTTPMethods,
        path: str,
        *,
        response_model: type[Model] | type[list[Model]] | None = None,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        headers: dict[str, str] | None = None,
        json: Model | Any | None = None,
        xml: XMLModel | str | bytes | None = None,
        response_model_kwargs: dict[str, Any] | None = None,
        request_model_kwargs: dict[str, Any] | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        max_retries: int | None = None,
        error_map: dict[int, ErrorStatus] | None = None,
    ) -> Model | list[Model] | Response:
        """
        Construct and send an HTTP POST request.

        Args:
            method:
                The HTTP method used to make the call.
            path:
                URL to query.
            response_model:
                Pydantic model to coerce the response into.
            response_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                un-marshalling the response data.
            request_model_kwargs:
                Keyword arguments to pass to Pydantic/Pydantic-XML as part of
                marshalling the body of the data into the request.
            params:
                Request query parameters.
            content:
                Raw body of the request.
            data:
                URL form-encoded body for the request.
            json:
                Data object to marshal into JSON. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            xml:
                Data object to marshal into XML. Content passed with this parameter
                will also set the ``Content-Type`` header to ``application/json``.
            files:
                A dictionary of upload files to include in the body of the request.
            headers:
                Request-specific headers.
            cookies:
                Request-specific cookies.
            auth:
                Request-specific authentication.
            follow_redirects:
                Should the client follow any redirects?
            timeout:
                Request-specific timeout settings.
            extensions:
                Any additional httpx extensions to pass to the client.
            max_retries:
                The maximum number of retries to attempt before giving up. Overloads
                the client default.
            error_map:
                Replaces the client error map with this one instead.

        Returns:
            Returns the HTTPX Response object if no response_model is specified. If a
            response_model _is_ specified, then the response will be coerced into the
            response model and the instance of the model will be returned.
        """
        max_retries = max_retries if max_retries else self._retry_max
        error_map = self._error_map if error_map is None else error_map
        response_model_kwargs = (
            {} if response_model_kwargs is None else response_model_kwargs
        )

        # Perform any pre-processing necessary on the request.
        kwargs = self._request_pre_process(
            method=method,
            url=path,
            params=params,
            content=content,
            data=data,
            files=files,
            json=json,
            xml=xml,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
            request_model_kwargs=request_model_kwargs,
        )

        # Build the initial request and initialize the counter.
        request = self._client.build_request(**kwargs)
        request_counter = 0

        # While the number of requests being performed is less than or equal to the
        # maximum number allowed, then keep calling the API.
        while request_counter <= max_retries:
            request_counter += 1
            response = self._client.send(
                request, auth=auth, follow_redirects=follow_redirects
            )

            # If the response is ok, then we should return the response.  If a model is
            # presented to us, then we will pass the model to the unmarshal utility to
            # handle transitioning the data into the expected class.
            if response.status_code == codes.OK and response_model:
                return unmarshal(
                    response=response,
                    model=response_model,
                    json_model_kwargs=self._json_model_kwargs | response_model_kwargs,
                    xml_model_kwargs=self._xml_model_kwargs | response_model_kwargs,
                )

            # If no model was passed, then simply return the response object.
            elif response.status_code == codes.OK:
                return response

            # As the response wasn't ok, let's grab the ErrorStatus object that relates
            # to the status code that we got and determine the next steps.
            status = error_map[response.status_code]

            # If the status code is retryable, then pass the response to the retry
            # handler to perform any optional transformation.  Then sleep the amount
            # if time determined by the status code and then continue to the next
            # iteration.
            if status.retry:
                request = self._retry_request(response)
                timer = random.uniform(0, status.jitter) + (
                    request_counter * status.backoff
                )
                sleep(timer)
                continue

            # Otherwise we will want to raise the error as specified by the error map
            error_obj = None
            raise status.exception(
                response=response, template=status.template, obj=error_obj
            )

        # If too many attempts were made, then raise a retry error.
        raise RetryError(url=str(path), method=method, attempts=request_counter)

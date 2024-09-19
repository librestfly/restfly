"""
Endpoints
=========

.. autoclass:: APIEndpoint
    :members:
    :private-members:
"""

from typing import Optional, Union, Dict
from box import Box, BoxList
from requests import Response
from .session import APISession


class APIEndpoint:  # noqa: PLR0903
    """
    APIEndpoint is the base model for which all API endpoint classes are
    sired from.  The main benefit is the ability to use the http request methods that
    are attached to this base class.  This allows for keeping common CRUD-type calls
    together with minimal manual URL munging.

    Attributes:
        _path (str):
            The URI path to append to the base path as is specified in the
            APISession object.  This can become quite useful if most of the
            CRUD follows the same pathing.  It is only used when using the
            APIEndpoint verbs (_get, _post, _put, etc.).
        _box (bool):
            An endpoint-specific version of `APISession._box`.
        _box_attrs (bool):
            An endpoint-specific version of `APISession._box_attrs`.
        _conv_json (bool):
            An endpoint-specific version of `APISession._conv_json`.

    Args:
        api (APISession):
            The APISession (or sired child) instance that the endpoint will
            be using to perform calls to the API.
    """

    _path: str = None
    _box: bool = None
    _conv_json: bool = None
    _box_attrs: Dict = None

    def __init__(self, api: APISession):
        self._api = api
        self._log = api._log

    def _req(
        self, method: str, path: Optional[str] = None, **kwargs
    ) -> Union[Box, BoxList, Response]:
        """
        An abstraction of the APISession._req method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api._req``.

        Args:
            method (str):
                The HTTP method
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._req('GET', **kwargs)
        """
        if self._box:
            kwargs['box'] = kwargs.get('box', self._box)
        if self._box_attrs:
            kwargs['box_attrs'] = kwargs.get('box_attrs', self._box_attrs)
        if self._conv_json:
            kwargs['conv_json'] = kwargs.get('conv_json', self._conv_json)
        new_path = '/'.join([p for p in [self._path, path] if p])
        return self._api._req(method, new_path, **kwargs)  # noqa: PLW0212

    def _delete(
        self, path: Optional[str] = None, **kwargs
    ) -> Union[Box, BoxList, Response]:
        """
        An abstraction of the APISession.delete method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.delete``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._delete(**kwargs)
        """
        return self._req('DELETE', path, **kwargs)

    def _get(
        self, path: Optional[str] = None, **kwargs
    ) -> Union[Box, BoxList, Response]:
        """
        An abstraction of the APISession.get method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.get``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._get(**kwargs)
        """
        return self._req('GET', path, **kwargs)

    def _head(
        self, path: Optional[str] = None, **kwargs
    ) -> Union[Box, BoxList, Response]:
        """
        An abstraction of the APISession.head method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.head``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._head(**kwargs)
        """
        return self._req('HEAD', path, **kwargs)

    def _patch(
        self, path: Optional[str] = None, **kwargs
    ) -> Union[Box, BoxList, Response]:
        """
        An abstraction of the APISession.patch method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.patch``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._patch(**kwargs)
        """
        return self._req('PATCH', path, **kwargs)

    def _post(
        self, path: Optional[str] = None, **kwargs
    ) -> Union[Box, BoxList, Response]:
        """
        An abstraction of the APISession.post method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.post``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._post(**kwargs)
        """
        return self._req('POST', path, **kwargs)

    def _put(
        self, path: Optional[str] = None, **kwargs
    ) -> Union[Box, BoxList, Response]:
        """
        An abstraction of the APISession.put method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.put``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._put(**kwargs)
        """
        return self._req('PUT', path, **kwargs)

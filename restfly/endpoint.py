'''
Endpoints
=========

.. autoclass:: APIEndpoint
    :members:
    :private-members:
'''


class APIEndpoint(object):
    '''
    APIEndpoint is the base model for which all API endpoint classes are
    sired from.  The main benefit is the addition of the ``_check()``
    function from which it's possible to check the type & content of a
    variable to ensure that we are passing good data to the API.

    Args:
        api (APISession):
            The APISession (or sired child) instance that the endpoint will
            be using to perform calls to the API.
    '''
    _path = None

    def __init__(self, api):
        self._api = api
        self._log = api._log

    def _request(self, method, path=None, **kwargs):
        '''
        An abstraction of the APISession._request method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api._request``.

        Args:
            method (str):
                The HTTP method
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.
            retry_on (list, optional):
                A list of numeric response status codes to attempt retry on.
                This behavior is additive to the retry parameter in the
                exceptions.

        Returns:
            :obj:`requests.Response`:
                The response object from the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._request('GET', **kwargs)
        '''
        p = '/'.join([p for p in [self._path, path] if p])
        return self._api._request(method, p, **kwargs)

    def _delete(self, path=None, **kwargs):
        '''
        An abstraction of the APISession.delete method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.delete``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.
            retry_on (list, optional):
                A list of numeric response status codes to attempt retry on.
                This behavior is additive to the retry parameter in the
                exceptions.

        Returns:
            :obj:`requests.Response`:
                The response object from the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._delete(**kwargs)
        '''
        return self._request('DELETE', path, **kwargs)

    def _get(self, path=None, **kwargs):
        '''
        An abstraction of the APISession.get method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.get``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.
            retry_on (list, optional):
                A list of numeric response status codes to attempt retry on.
                This behavior is additive to the retry parameter in the
                exceptions.

        Returns:
            :obj:`requests.Response`:
                The response object from the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._get(**kwargs)
        '''
        return self._request('GET', path, **kwargs)

    def _head(self, path=None, **kwargs):
        '''
        An abstraction of the APISession.head method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.head``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.
            retry_on (list, optional):
                A list of numeric response status codes to attempt retry on.
                This behavior is additive to the retry parameter in the
                exceptions.

        Returns:
            :obj:`requests.Response`:
                The response object from the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._head(**kwargs)
        '''
        return self._request('HEAD', path, **kwargs)

    def _patch(self, path=None, **kwargs):
        '''
        An abstraction of the APISession.patch method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.patch``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.
            retry_on (list, optional):
                A list of numeric response status codes to attempt retry on.
                This behavior is additive to the retry parameter in the
                exceptions.

        Returns:
            :obj:`requests.Response`:
                The response object from the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._patch(**kwargs)
        '''
        return self._request('PATCH', path, **kwargs)

    def _post(self, path=None, **kwargs):
        '''
        An abstraction of the APISession.post method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.post``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.
            retry_on (list, optional):
                A list of numeric response status codes to attempt retry on.
                This behavior is additive to the retry parameter in the
                exceptions.

        Returns:
            :obj:`requests.Response`:
                The response object from the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._post(**kwargs)
        '''
        return self._request('POST', path, **kwargs)

    def _put(self, path=None, **kwargs):
        '''
        An abstraction of the APISession.put method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.put``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.
            retry_on (list, optional):
                A list of numeric response status codes to attempt retry on.
                This behavior is additive to the retry parameter in the
                exceptions.

        Returns:
            :obj:`requests.Response`:
                The response object from the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._put(**kwargs)
        '''
        return self._request('PUT', path, **kwargs)
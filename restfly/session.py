'''
Sessions
========

.. autoclass:: APISession
    :members:
    :private-members:
'''
import requests, sys, time
from .errors import *
from . import __version__

class APISession(object):
    '''
    The APISession class is the base model for APISessions for different
    products and applications.  This is the model that the APIEndpoints
    will be grafted onto and supports some basic wrapping of standard HTTP
    methods on it's own.

    Attributes:
        _backoff (float):
            The default backoff timer to use when retrying.  The value is either
            a float or integer denoting the number of seconds to delay before
            the next retry attempt.  The number will be multiplied by the number
            of retries attempted.
        _error_map (dict):
            The error mapping detailing what HTTP response code should throw
            what kind of error.  Specifically meant to be overloadable based on
            need.
        _identity (str):
            An optional identifier for the application to discern it amongst
            other API calls.
        _proxies (dict):
            A dictionary detailing what proxy should be used for what transport
            protocol.  This value will be passed to the session object after it
            has been either attached or created.  For details on the structure
            of this dictionary, consult the
            :requests:`proxies section of the Requests documentation.<user/advanced/#proxies>`
        _restricted_paths (list):
            A list of paths (not complete URIs) that if seen be the
            :obj:`_request` method will not pass the query params or the request
            body into the logging facility.  This should generally be used for
            paths that are sensitive in nature (such as logins).
        _retries (int):
            The number of retries to make before failing a request.  The
            default is 3.
        _session (requests.Session):
            Provide a pre-built session instead of creating a requests session
            at instantiation.
        _url (str):
            The base URL path to use.  This should generally be a string value
            denoting the first half of the URI.  For example,
            ``https://httpbin.org`` or ``https://example.api.site/api/2``.  The
            :obj:`_request` method will join this string with the incoming path
            to construct the complete URI.  Note that the two strings will be
            joined with a backslash ``/``.
    '''
    _url = None
    _retries = 3
    _backoff = 1
    _proxies = None
    _identity = None
    _lib_identity = 'Restfly'
    _lib_version = __version__
    _restricted_paths = list()
    _error_map = {
        400: BadRequestError,
        401: UnauthorizedError,
        403: ForbiddenError,
        404: NotFoundError,
        405: InvalidMethodError,
        406: NotAcceptableError,
        407: ProxyAuthenticationError,
        408: RequestTimeoutError,
        409: RequestConflictError,
        410: NoLongerExistsError,
        411: LengthRequiredError,
        412: PreconditionFailedError,
        413: PayloadTooLargeError,
        414: URITooLongError,
        415: UnsupportedMediaTypeError,
        416: RangeNotSatisfiableError,
        417: ExpectationFailedError,
        418: TeapotResponseError,
        420: TooManyRequestsError,
        421: MisdirectRequestError,
        425: TooEarlyError,
        426: UpgradeRequiredError,
        428: PreconditionRequiredError,
        429: TooManyRequestsError,
        431: RequestHeaderFieldsTooLargeError,
        451: UnavailableForLegalReasonsError,
        500: ServerError,
        501: MethodNotImplementedError,
        502: BadGatewayError,
        503: ServiceUnavailableError,
        504: GatewayTimeoutError,
        510: NotExtendedError,
        511: NetworkAuthenticationRequiredError,
    }

    def __init__(self, **kw):
        '''
        APISession initialization

        Args:
            backoff (float, optional):
                If a 429 response is returned, how much do we want to backoff
                if the response didn't send a Retry-After header.
            identity (str, optional):
                An optional identifier for the application to discern it amongst
                other API calls.
            proxies (dict, optional):
                A dictionary detailing what proxy should be used for what
                transport protocol.  This value will be passed to the session
                object after it has been either attached or created.  For
                details on the structure of this dictionary, consult the
                :requests:`proxies <user/advanced/#proxies>` section of the
                Requests documentation.
            retries (int, optional):
                The number of retries to make before failing a request.  The
                default is 3.
            session (requests.Session, optional):
                Provide a pre-built session instead of creating a requests
                session at instantiation.
            url (str, optional):
                The base URL that the paths will be appended onto.
        '''
        # Assign the kw arguments to the private attributes.
        self._url = kw.get('url', self._url)
        self._retries = int(kw.get('retries', self._retries))
        self._backoff = float(kw.get('backoff', self._backoff))
        self._proxies = kw.get('proxies', self._proxies)
        self._identity = kw.get('identity', self._identity)

        # Create the logging facility
        self._log = logging.getLogger('{}.{}'.format(
            self.__module__, self.__class__.__name__))

        # Initiate the session builder.
        self._build_session(kw.get('session'))

    def _build_session(self, session=None):
        '''
        The session builder.  User-agent strings, cookies, headers, etc that
        should persist for the session should be initiated here.  The session
        builder is called as part of the APISession constructor.

        Args:
            session (requests.Session, optional):
                If a session object was passed to the constructor, then this
                would contain a session, otherwise a new one is created.

        Returns:
            :obj:`None`

        Examples:
            Extending the session builder to use basic auth:

            >>> class ExampleAPI(APISession):
            ...     def _build_session(self, session=None):
            ...         APISession._build_session(self, session)
            ...         self._session.auth = (self._username, self._password)
        '''
        # link up the session to either the one passed or create a new session.
        self._session = session if session else requests.Session()

        # If proxy support is needed, update the proxies in the session.
        if self._proxies:
            self._session.proxies.update(self._proxies)

        # Update the User-Agent string with the information necessary.
        self._session.headers.update({
            'User-Agent': '{} ({}/{}; Restfly/{}; Python/{})'.format(
                # If the identity was set, then use it, otherwise use the libs.
                self._identity if self._identity else self._lib_identity,

                # The Library identity and version
                self._lib_identity,
                self._lib_version,

                # Restfly's version
                __version__,

                # The python version information
                '.'.join([str(i) for i in sys.version_info][0:3])),
        })

    def _resp_error_check(self, response): #stub
        '''
        If there is a need for additional error checking (for example within the
        JSON response) then overload this method with the necessary checking.

        Args:
            response (request.Response):
                The response object.

        Returns:
            :obj:`requests.Response`:
                The response object.
        '''
        return response

    def _retry_request(self, response, retries, kwargs): #stub
        '''
        A method to be overloaded to return any modifications to the request
        upon retries.  By default just passes back what was send in the same
        order.

        Args:
            response (request.Response):
                The response object
            retries (int):
                The number of retries that have been performed.
            kwargs (dict):
                The keyword arguments that were passed to the request.

        Returns:
            :obj:`dict`:
                The keyword arguments
        '''
        return kwargs

    def _request(self, method, path, **kwargs):
        '''
        The requests session base request method.  This is considered internal
        as it's generally recommended to use the bespoke methods for each HTTP
        method.

        Args:
            method (str): The HTTP method
            path (str): The URI path to append to the base path.
            **kwargs (dict): The keyword arguments to pass to the requests lib.

        Returns:
            :obj:`requests.Response`:
                The response object from the requests lib.

        Examples:
            >>> api = APISession()
            >>> resp = api._request('GET', '/')
        '''
        retries = 0
        err = None
        while retries <= self._retries:
            if (('params' in kwargs and kwargs['params'])
              or ('json' in kwargs and kwargs['json'])):
                if path not in self._restricted_paths:
                    # If the path is not one of the paths that would contain
                    # sensitive data (such as login information) then pass the
                    # log on unredacted.
                    self._log.debug('path={}, query={}, body={}'.format(
                        path, kwargs.get('params', {}), kwargs.get('json', {})))
                else:
                    # The path was a restricted path, generate the log, however
                    # redact the information.
                    self._log.debug('path={}, query={}, body={}'.format(
                        path, 'REDACTED', 'REDACTED'))

            # Make the call to the API and pull the status code.
            resp = self._session.request(method,
                '{}/{}'.format(self._url, path), **kwargs)
            status = resp.status_code

            if status in self._error_map.keys():
                # If a status code that we know about has returned, then we will
                # want to raise the appropriate Error.
                err = self._error_map[status]
                if err.retryable:
                    # If the APIError fetched is retryable, we will want to
                    # attempt to retry our call.  If we see the "Retry-After"
                    # header, then we will respect that.  If no "Retry-After"
                    # header exists, then we will use the _backoff attribute to
                    # build a back-off timer based on the number of retries we
                    # have already performed.
                    retries += 1
                    time.sleep(resp.headers.get(
                        'retry-after', retries * self._backoff))

                    # The need to potentially modify the request for subsequent
                    # calls is the whole reason that we aren't using the default
                    # Retry logic that urllib3 supports.
                    kwargs = self._retry_request(resp, retries, kwargs)
                    continue
                else:
                    raise err(resp, retries=retries)

            elif status >= 200 and status <= 299:
                # As everything looks ok, lets pass the response on to the error
                # checker and then return the response.
                return self._resp_error_check(resp)

            else:
                # If all else fails, raise an error stating that we don't even
                # know whats happening.
                raise APIError(resp, retries=retries)
        raise err(resp, retries=retries)

    def get(self, path, **kwargs):
        '''
        Initiates an HTTP GET request using the specified path.  Refer to
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to the Requests library.

        Returns:
            :obj:`requests.Response`

        Examples:
            >>> api = APISession()
            >>> resp = api.get('/')
        '''
        return self._request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        '''
        Initiates an HTTP POST request using the specified path.  Refer to the
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appented onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to the Requests library.

        Returns:
            :obj:`requests.Response`

        Examples:
            >>> api = APISession()
            >>> resp = api.post('/')
        '''
        return self._request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        '''
        Initiates an HTTP PUT request using the specified path.  Refer to the
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to the Requests library.

        Returns:
            :obj:`requests.Response`

        Examples:
            >>> api = APISession()
            >>> resp = api.put('/')
        '''
        return self._request('PUT', path, **kwargs)

    def patch(self, path, **kwargs):
        '''
        Initiates an HTTP PATCH request using the specified path.  Refer to the
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to the Requests library.

        Returns:
            :obj:`requests.Response`

        Examples:
            >>> api = APISession()
            >>> resp = api.patch('/')
        '''
        return self._request('PATCH', path, **kwargs)

    def delete(self, path, **kwargs):
        '''
        Initiates an HTTP DELETE request using the specified path.  Refer to the
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to the Requests library.

        Returns:
            :obj:`requests.Response`

        Examples:
            >>> api = APISession()
            >>> resp = api.delete('/')
        '''
        return self._request('DELETE', path, **kwargs)

    def head(self, path, **kwargs):
        '''
        Initiates an HTTP HEAD request using the specified path.  Refer to the
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to the Requests library.

        Returns:
            :obj:`requests.Response`

        Examples:
            >>> api = APISession()
            >>> resp = api.head('/')
        '''
        return self._request('HEAD', path, **kwargs)


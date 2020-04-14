'''
Sessions
========

.. autoclass:: APISession
    :members:
    :private-members:
'''
import requests, sys, time, warnings, platform, json
from requests.exceptions import (
    ConnectionError as RequestsConnectionError,
    RequestException as RequestsRequestException
)
from .utils import dict_merge
from .errors import *
from . import __version__

try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

class APISession(object):
    '''
    The APISession class is the base model for APISessions for different
    products and applications.  This is the model that the APIEndpoints
    will be grafted onto and supports some basic wrapping of standard HTTP
    methods on it's own.

    Attributes:
        _build (str):
            The build number/version of the integration.
        _backoff (float):
            The default backoff timer to use when retrying.  The value is either
            a float or integer denoting the number of seconds to delay before
            the next retry attempt.  The number will be multiplied by the number
            of retries attempted.
        _base_error_map (dict):
            The error mapping detailing what HTTP response code should throw
            what kind of error.  As this is the base mapping, overloading this
            would remove any pre-set error mappings.
        _error_map (dict):
            The error mapping detailing what HTTP response code should throw
            what kind of error.  This error map will overload specific error
            mappings.
        _lib_name (str):
            The name of the library.
        _lib_version (str):
            The version of the library.
        _product (str):
            The product name for the integration.
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
        _ssl_verify (bool):
            Should SSL verification be performed?  If not, then inform requests
            that we don't want to use SSL verification and suppress the SSL
            certificate warnings.
        _timeout (int):
            The number of seconds to wait with no data returned before declaring
            the request as stalled and timing-out the request.
        _url (str):
            The base URL path to use.  This should generally be a string value
            denoting the first half of the URI.  For example,
            ``https://httpbin.org`` or ``https://example.api.site/api/2``.  The
            :obj:`_request` method will join this string with the incoming path
            to construct the complete URI.  Note that the two strings will be
            joined with a backslash ``/``.
        _vendor (str):
            The vendor name for the integration.
    '''
    _url = None
    _retries = 3
    _backoff = 1
    _proxies = None
    _ssl_verify = True
    _lib_name = 'Restfly'
    _lib_version = __version__
    _restricted_paths = list()
    _vendor = 'unknown'
    _product = 'unknown'
    _build = __version__
    _adaptor = None
    _timeout = None
    _error_map = dict()
    _base_error_map = {
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

    def __enter__(self):
        '''
        Context Manager __enter__ built-in method. See PEP-343 for more details.
        '''
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        '''
        Context Manager __exit__ built-in method. See PEP-343 for more details.
        '''
        return self._deauthenticate()

    def __init__(self, **kwargs):
        '''
        APISession initialization

        Args:
            adaptor (Object, optional):
                A Requests Session adaptor to bind to the session object.
            backoff (float, optional):
                If a 429 response is returned, how much do we want to backoff
                if the response didn't send a Retry-After header.
            build (str, optional):
                The build number to put into the User-Agent string.
            product (str, optional):
                The product name to put into the User-Agent string.
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
            ssl_verify (bool, optional):
                If SSL Verification needs to be disabled (for example when using
                a self-signed certificate), then this parameter should be set to
                ``False`` to disable verification and mask the Certificate
                warnings.
            url (str, optional):
                The base URL that the paths will be appended onto.
            vendor (str, optional):
                The vendor name to put into the User-Agent string.
        '''
        # Construct the error map from the base mapping, then overload the map
        # with anything specified in the error map parameter and then store the
        # final result in the error map parameter.  This allows for overloading
        # specific items if necessary without having to re-construct the whole
        # map.
        self._error_map = dict_merge(self._base_error_map, self._error_map)

        # Assign the kw arguments to the private attributes.
        self._url = kwargs.get('url', self._url)
        self._retries = int(kwargs.get('retries', self._retries))
        self._backoff = float(kwargs.get('backoff', self._backoff))
        self._proxies = kwargs.get('proxies', self._proxies)
        self._ssl_verify = kwargs.get('ssl_verify', self._ssl_verify)
        self._adaptor = kwargs.get('adaptor', self._adaptor)
        self._vendor = kwargs.get('vendor', self._vendor)
        self._product = kwargs.get('product', self._product)
        self._build = kwargs.get('build', self._build)
        self._error_func = kwargs.get('error_func', api_error_func)
        self._timeout = kwargs.get('timeout', self._timeout)

        # Create the logging facility
        self._log = logging.getLogger('{}.{}'.format(
            self.__module__, self.__class__.__name__))

        # Initiate the session builder.
        self._build_session(**kwargs)
        self._authenticate(**kwargs)

    def _build_session(self, **kwargs):
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
            ...         super(APISession, self)._build_session(**kwargs)
            ...         self._session.auth = (self._username, self._password)
        '''
        uname = platform.uname()
        # link up the session to either the one passed or create a new session.
        self._session = kwargs.get('session', requests.Session())

        # If proxy support is needed, update the proxies in the session.
        if self._proxies:
            self._session.proxies.update(self._proxies)

        # If the SSL verification is disabled then we will need to disable
        # verification in the requests session and we also want to mask the
        # certificate warnings.
        if not self._ssl_verify:
            self._session.verify = self._ssl_verify
            warnings.filterwarnings('ignore', 'Unverified HTTPS request')

        # Update the User-Agent string with the information necessary.
        self._session.headers.update({
            'User-Agent': ' '.join([
                'Integration/1.0 ({}; {}; Build/{})'.format(

                    # The vendor name for the integration
                    self._vendor,

                    # The product name of the integration
                    self._product,

                    # The build of the integration
                    self._build
                ),
                '{}/{} (Restfly/{}; Python/{}; {}/{})'.format(

                    # The name of the library being used
                    self._lib_name,

                    # The version of the library being used
                    self._lib_version,

                    # The version of Restfly
                    __version__,

                    # The python version string
                    '.'.join([str(i) for i in sys.version_info][0:3]),

                    # The source OS
                    uname[0],

                    # The source Arch
                    uname[-2]
                ),
            ])
        })

    def _authenticate(self, **kwargs):
        '''
        '''
        pass

    def _deauthenticate(self, **kwargs):
        '''
        '''
        pass

    def _resp_error_check(self, response, **kwargs): #stub
        '''
        If there is a need for additional error checking (for example within the
        JSON response) then overload this method with the necessary checking.

        Args:
            response (request.Response):
                The response object.
            **kwargs (dict):
                The request keyword arguments.

        Returns:
            :obj:`requests.Response`:
                The response object.
        '''
        return response

    def _retry_request(self, response, retries, **kwargs): #stub
        '''
        A method to be overloaded to return any modifications to the request
        upon retries.  By default just passes back what was send in the same
        order.

        Args:
            response (request.Response):
                The response object
            retries (int):
                The number of retries that have been performed.
            **kwargs (dict):
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
            method (str):
                The HTTP method
            path (str):
                The URI path to append to the base path.
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
            >>> api = APISession()
            >>> resp = api._request('GET', '/')
        '''
        err = None
        retries = 0

        # If retry_on is specified, then we will populate the retry_codes
        # variable with a list of numeric status codes to additionally retry on.
        # This is helpful if the API in question doesn't always behave in a
        # consistent manner.
        retry_codes = kwargs.pop('retry_on', list())

        # While the number of retries is less than the retry limit, loop.  As we
        # will be returning from within the loop if we receive a successful
        # response or a non-retryable error, the loop should only be handling
        # the retries themselves.
        while retries <= self._retries:
            # Check to see if the path is a relative path or a full path  If
            # we were able to successfully parse a network location using
            # urlparse, then we will assume that this is a full path and pass
            # the URL as-is.  If it's a relative path, then we will append the
            # baseurl to the path.  In either case, the constructed uri string
            # is what we will be using for the rest of the method for making
            # the actual calls.
            if len(urlparse(path).netloc) > 0:
                uri = path
            else:
                uri = '{}/{}'.format(self._url, path)

            if (('params' in kwargs and kwargs['params'])
              or ('json' in kwargs and kwargs['json'])):
                if path not in self._restricted_paths:
                    # If the path is not one of the paths that would contain
                    # sensitive data (such as login information) then pass the
                    # log on unredacted.
                    self._log.debug(json.dumps({
                            'method': method,
                            'url': uri,
                            'params': kwargs.get('params', {}),
                            'body': kwargs.get('json', {})
                        })
                    )
                else:
                    # The path was a restricted path, generate the log, however
                    # redact the information.
                    self._log.debug(json.dumps({
                            'method': method,
                            'url': uri,
                            'params': 'REDACTED',
                            'body': 'REDACTED'
                        })
                    )

            # Make the call to the API and pull the status code.
            try:
                resp = self._session.request(method, uri,
                    timeout=self._timeout, **kwargs)
                status = resp.status_code

            # Here we will catch any underlying exceptions thrown from the
            # requests library, log them, iterate the retry counter, then
            # release the attempt for the next iteration.
            except (RequestsConnectionError, RequestsRequestException) as err:
                self._log.error('Requests Library Error: {}'.format(str(err)))
                time.sleep(1)
                retries += 1

            # The following code will run when a request successfully returned.
            else:
                if status in self._error_map.keys():
                    # If a status code that we know about has returned, then we
                    # will want to raise the appropriate Error.
                    err = self._error_map[status]
                    if err.retryable or status in retry_codes:
                        # If the APIError fetched is retryable, we will want to
                        # attempt to retry our call.  If we see the
                        # "Retry-After" header, then we will respect that.  If
                        # no "Retry-After" header exists, then we will use the
                        # _backoff attribute to build a back-off timer based on
                        # the number of retries we have already performed.
                        retries += 1
                        time.sleep(resp.headers.get(
                            'retry-after', retries * self._backoff))

                        # The need to potentially modify the request for
                        # subsequent calls is the whole reason that we aren't
                        # using the default Retry logic that urllib3 supports.
                        kwargs = self._retry_request(resp, retries, **kwargs)
                        continue
                    else:
                        raise err(resp, retries=retries, func=self._error_func)

                elif status >= 200 and status <= 299:
                    # As everything looks ok, lets pass the response on to the
                    # error checker and then return the response.
                    return self._resp_error_check(resp, **kwargs)

                else:
                    # If all else fails, raise an error stating that we don't
                    # even know whats happening.
                    raise APIError(resp, retries=retries, func=self._error_func)
        raise err(resp, retries=retries, func=self._error_func)

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
                The path to be appended onto the base URL for the request.
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


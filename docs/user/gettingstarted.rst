.. _gettingstarted:

Getting Started
===============

.. image:: https://live.staticflickr.com/3452/3214601797_112f2ea202_b.jpg

Looking to hit the ground running?  This page gives a good primer to aid in
getting started with RESTfly.

First, make sure that:

* RESTfly is :ref:`installed <install>`
* RESTfly is up-to-date

Now lets get started with a few examples:

Calling a Simple Unauthenticated API
------------------------------------

For the examples in this quickstart, we will be using
`HTTPbin <https://httpbin.org/>`_ as our basic API to interact with.  It removes
more complex things like authentication from the mix for now and instead allows
us to realize how to build the scaffolding quite quickly.

Now to get started, lets first import the ``APISession`` class::

    >>> from restfly.session import APISession

Now lets subclass APISession and start making our HTTPBin library.  In this
case all we will need to do to really get moving is to overload the ``_url``
parameter within the APISession class with the base path that we want to use::

    >>> class HTTPBin(APISession):
    ...     _url = 'https://httpbin.org'

Note that we don't put a trailing ``/`` in the URL path.  This is on purpose, as
RESTfly, will then join that _url string to the request calls.  If this sounds
confusing, then lets just show a couple of examples using the built-in methods
available to us::

    >>> httpbin = HTTPBin()
    >>> resp = httpbin.get('get') # GET https://httpbin.org/get
    >>> resp = httpbin.patch('patch') # PATCH https://httpbin.org/patch
    >>> resp = httpbin.post('post') # POST https://httpbin.org/post
    >>> resp = httpbin.put('put') # PUT https://httpbin.org/put
    >>> resp = httpbin.delete('delete') # DELETE https://httpbin.org/delete

The response that has been returned in each of these cases is a Requests
Response object, just as if you were to make a
``resp = requests.get('https://httpbin.org/get')`` call.  This may not seem like
much of an improvement at first, but lets take this a step further now and wrap
some of the paths into class as well::

    >>> class HTTPBin(APISession):
    ...     _url = 'https://httpbin.org'
    ...
    ...     def get_status(self, code: int) -> dict:
    ...         return self.get('status/{}'.format(code)).json()
    >>>
    >>> httpbin = HTTPBin()
    >>> resp = httpbin.get_status(200)

Awesome!  We've successfully wrapped the status API path and now we will get a
Python dictionary as a response instead of a raw Response object like before.

Using APIEndpoint
-----------------

The next step in our journey of discovery brings us to the ``APIEndpoint``
class.  This class is designed to make wrapping logical sections of the API into
something that we can logically separate.  A good general example here would be
common CRUD operations for a given model.  Lets start with this example::

    >>> from restfly.endpoint import APIEndpoint
    >>>
    >>> class UserAPI(APIEndpoint):
    ...     _path = 'users'
    ...
    ...     def create(self, username: str, password: str, name: str) -> None:
    ...         '''POST https://exmaple.com/api/users'''
    ...         return self._post(json={
    ...             'username': username,
    ...             'password': password,
    ...             'name': name
    ...         }).json() # Returns user id
    ...
    ...     def update(self, id: int, **kwargs) -> dict:
    ...         '''PATCH https://exmaple.com/api/users/{id}'''
    ...         return self._patch(str(id), json=kwargs).json()
    ...         # Returns user id
    ...
    ...     def delete(self, id: int) -> dict:
    ...         '''DELETE https://exmaple.com/api/users/{id}'''
    ...         return self._delete(str(id)).json()
    ...
    ...     def list(self) -> dict:
    ...         '''GET https://exmaple.com/api/users'''
    ...         return self._get().json()

It covers a the basics of CRUD operations for the ``users`` endpoint.  Now we
just need to link it up to an APISession class so that it's usable.  Doing so
is fairly simple::

    >>> from restfly.session import APISession
    >>>
    >>> class ExampleAPI(APISession):
    ...     _url = 'https://example.com/api'
    ...
    ...     @property
    ...     def users(self) -> UserAPI:
    ...         return UserAPI(self)

If you note, we just define the property of *users* and then have it return the
``UserAPI`` class.  Eagle-eyed readers may note that we're also passing the
``ExampleAPI`` object while we're returning an instance of ``UserAPI``.  This is
how we're linking the two together and ultimately is what ``self._api`` is
within the **APIEndpoint** class.

To use this, we will call this just like we did with the HTTPbin example,
however we will now have the ``users`` parameter to use::

    >>> api = ExampleAPI()
    >>> user_id = api.users.create('jsmith', 'sekretsquirrel', 'John Smith')
    >>> user_id = api.users.update(user_id, password='n3wsquirrel')
    >>> api.users.delete(user_id)

As you can imagine, we can keep bolting on APIEndpoints to the APISession as
necessary and map out the API.

Using Authentication
--------------------

Authentication is the next logical step here, and how it's implemented will
likely vary significantly depending the API and how auth is handled.  For
simplicities sake, we will be making the assumption of a simple API key that
will be provided as an additional header with every call.  To handle this, we
will need to make a couple of changes:

* We will want to overload the constructor in order to provide the API key
* We will want to overload the session builder to add the auth header.

The resulting code will look like this:

    >>> class ExampleAPI(APISession):
    ...     _url = 'https://example.com/api'
    ...
    ...     def __init__(self, api_key: str, **kwargs):
    ...         self._api_key = api_key
    ...         super(ExampleAPI, self).__init__(**kwargs)
    ...
    ...     def _build_session(self, **kwargs) -> None:
    ...         super(ExampleAPI, self)._build_session(**kwargs)
    ...         self._session.headers.update({
    ...             'X-API-Key': self._api_key,
    ...         })

As this is a stateless example above, there isn't any need to worry about
session tokens, cookies, etc.  However if there was, then we simply take
advantage of the cookiejar and session management that Requests gave us.
Below is a simple example using Basic Auth:

    >>> class ExampleAPI(APISession):
    ...     _url = 'https://exmaple.com/api'
    ...
    ...     def login(self, username: str, password: str) -> None:
    ...         self._session.auth = (username, password)
    ...
    ...     def logout(self) -> None:
    ...         self._session.auth = None

For something more involved using an API call, like needing to grab a session
token, you could perform the following:

    >>> class ExampleAPI(APISession):
    ...     _url = 'https://example.com/api'
    ...
    ...     def login(self, username: str, password: str) -> None:
    ...         token = self._api.post('auth',
    ...             json={
    ...                'user': username,
    ...                'password': password
    ...             }).json()['token']
    ...         self._session.headers.update({
    ...             'X-Session-Token': token,
    ...         })
    ...
    ...     def logout(self) -> None:
    ...         self._api.delete('auth')
    ...         self._session.headers.update({
    ...             'X-Session-Token': None
    ...         })

Please note that for cookies, generally letting the Requests Session object's
cookiejar handle the work is all you need.  While you can overload the Cookie
header, it's generally discouraged.


Context handling and authentication
----------------------------------

Now that we have a basic understanding of how to handle authentication within
the library, lets take this a step further.  It seems that routinely when folks
use the method of authentication handling mentioned above, that the developers
using the library will invariably forget to logout of the session that they
had created.  For session-based authentication systems, this can create a lot
of potential issues when you just let those sessions linger instead of properly
closing them.  Thankfully RESTfly has some built-in stubs that we can hook into
to facilitate authentication and de-authentication through context management.

In sort, we can take something like this:

    >>> api = ExampleAPI()
    >>> api.login(username, password)
    >>> ## DO STUFF
    >>> api.logout()

and make it work like this instead:

    >>> with ExampleAPI(username=username, password=password) as api:
    ...     ### DO STUFF

And the context management within the library will handle authentication and
de-authentication for you.  To convert (and merge together) the previous
examples into a single coherent example with context management, the code
would look similar to below:

    >>> class ExampleAPI(APISession):
    ...    _url = 'https://example.com/api'
    ...
    ...    def _authenticate(self, **kwargs) -> None:
    ...        # Get the username, password, and api_key from the keyword
    ...        # arguments passed to the constructor.
    ...        username = kwargs.pop('username', None)
    ...        password = kwargs.pop('password', None)
    ...        api_key = kwargs.pop('api_key', None)
    ...
    ...        # Check for the api_key parameter, and if set, use the API Key
    ...        # for stateless authentication.
    ...        if api_key:
    ...            self._session.headers.update({
    ...                'X-API-Key': api_key
    ...            })
    ...
    ...        # If a username and a password were passed instead of an API Key
    ...        # we will then use stateful authentication and get the token.
    ...        elif username and password:
    ...            token = self.post('auth', json={
    ...                'username': username,
    ...                'password': password
    ...            })
    ...            self._session.headers.update({
    ...                'X-Session-Token': token
    ...            })
    ...
    ...        # If no stateless or stateful authentication mechanisms were
    ...        # passed, then we will send a warning log message
    ...        else:
    ...            self._log.warn('Starting an unauthenticated session')
    ...
    ...    def _deauthenticate(self, **kwargs) -> None:
    ...        if self._session.headers.get('X-Session-Token'):
    ...            self.delete('auth')
    ...            self._session.headers.update({'X-Session-Token': None})

Alrighty, so now we have authentication handled using the out-of-the-box stubs
to support it.  This means that we can now support authentication like so:

    >>> ## Session authentication
    >>> api = ExampleAPI(username=username, password=password)

    >>> ## API Key authentication
    >>> api = ExampleAPI(api_key=api_key)

    >>> ## Session auth with context management
    >>> with ExampleAPI(username=username, password=password) as api:
    ...     ### DO STUFF HERE

Now, what about the existing code that we have lying around already using this
library the old way above?  Well to support this code, we would add those old
methods back into the model like so:

    >>> class ExampleAPI(APISession):
    ...    def login(self, username: str, password: str) -> None:
    ...        self._authenticate({'username': username, 'password': password})
    ...
    ...    def logout(self) -> None:
    ...        self._deauthenticate()

It seems like a bit more than before, however this new example handles session
auth, api keys, and supports backwards compatibility to the previous examples.
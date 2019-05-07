.. _quickstart:

Quickstart
==========

.. image:: https://live.staticflickr.com/3452/3214601797_112f2ea202_b.jpg

Looking to hit the ground running?  This page gives a good primer to aid in
getting started with RESTfly.

First, make sure that:

* RESTfly is :ref:`installed <install>`
* RESTfly is :ref:`up-to-date <updates>`

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
    ...     def get_status(self, code):
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
    ...     def create(self, username, password, name):
    ...         '''POST https://exmaple.com/api/users'''
    ...         return self._api.post('users', json={
    ...             'username': username,
    ...             'password': password,
    ...             'name': name
    ...         }).json() # Returns user id
    ...
    ...     def update(self, id, **kwargs):
    ...         '''PATCH https://exmaple.com/api/users/{id}'''
    ...         return self._api.patch('users/{}'.format(id),
    ...             json=kwargs).json() # Returns user id
    ...
    ...     def delete(self, id):
    ...         '''DELETE https://exmaple.com/api/users/{id}'''
    ...         return self._api.delete('users/{}'.format(id)).json()
    ...
    ...     def list(self):
    ...         '''GET https://exmaple.com/api/users'''
    ...         return self._api.get('users').json()

It covers a the basics of CRUD operations for the ``users`` endpoint.  Now we
just need to link it up to an APISession class so that it's usable.  Doing so
is fairly simple::

    >>> from restfly.session import APISession
    >>>
    >>> class ExampleAPI(APISession):
    ...     _url = 'https://example.com/api'
    ...
    ...     @property
    ...     def users(self):
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
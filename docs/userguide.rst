User Guide
==========

Looking to hit the ground running?  This page gives a good primer to get you started with Restfly.


Installing RESTfly
------------------

Install RESTFly using your preferred package tooling:

With uv:

.. code:: bash

    uv add restfly

With pip:

.. code:: bash

    pip install restfly

Or event poetry:

.. code:: bash

    poetry add restfly


Calling a simple Unauthenticated API
------------------------------------

For the examples in this quickstart, we will be using `HTTPBin <https://httpbin.org>`_ as our basic API to interact
with.  This allows us to discuss things like authentication later and instead allows us to focus on the coding patterns
you should expect to see within your library codebase.

At a high level, RESTFly breaks things up into 2 primary structures that are generally required. You'll have your
client class that handles the basic authentication, houses the HTTPX session, and is the lower-level interaction point
with the API. From there you'll have one or many endpoint classes that point to either a specific endpoint or logical
grouping of endpoints and expose the parameters that is expected for each action and optionally marshals the data
to/from the native format.

.. mermaid::

    flowchart LR
        client@{ shape: rounded, label: "API Client" }
        endpoint@{ shape: docs, label: "API Endpoints"}
        client-->endpoint


To start, lets create a basic client and attach it to the status API. We also want to allow the caller to pass the
status code that they wish into the method. To accomplish this, we'd have something like this:

.. code:: python
    :number-lines:

    from httpx import Response
    from restfly import APIClient, APIEndpoint

    class StatusCodesAPI(APIEndpoint):
        _path = "/status"

        def get(self, status_code: int) -> Response:
            return self._get(f"/{status_code}")

    class HTTPBinClient(APIClient):
        _base_url = "https://httpbin.org"

        codes: StatusCodesAPI

From here we can discuss a few things. Firstly you'll notice the ``_base_url`` attribute pointing the client to the
base URL. This parameter informs RESTFly what the root URL is for all endpoints, so if it needed to have a path as
well, just ensure it's added to the base url attribute.

Next thing to talk about is in the APIEndpoint-based class we had created named ``StatusCodesAPI``. As you can see,
there is a ``_path`` attribute that acts as a prefix for all of the methods that we will be building within the
endpoint. While setting this is optional, it allows us to write all of the methods from the context of that prefix,
making the class itself potentially quite reusable if the same action structures are used through-out the codebase.

Lastly the ``get()`` method itself doesn't need to be complicated, as were passing the raw response object from HTTPX
back as the return. All we needed to do here is inform the HTTPX how to use the integer value that we collected.

Putting all of this together with the following python code using the library...

.. code:: python
    :number-lines:

    client = HTTPBinClient()
    resp = client.codes.get(200)

... will call ``GET https://httpbin.org/status/200`` and return the Response object. Keep in mind you can have any
number of actions and endpoints associated to a client.

Using Pydantic with RESTFly
---------------------------

Baking in support to use Pydantic and Pydantic-XML was one of the primary reasons for the rewrite. Previous usage of
Python-box was only sufficient for toy use-cases and ended up causing more headaches than it was worth. We took a lot
if inspiration from how FastAPI works in this regard and designed the model coercion to work in a similar way.

Starting with formatting the response into a pydantic model, we will want to define the model that we expect. Looking
at the HTTPBin methods API, the model would look something like this:

.. code:: python
    :number-lines:

    from pydantic import BaseModel

    class HTTPBinResponse(BaseModel):
        args: dict[str, str]
        headers: dict[str, str]
        origin: str
        url: str

In order to use that model within the library, lets create a new endpoint and use the ``response_model`` parameter.

.. code:: python
    :number-lines:

    class MethodsAPI(APIEndpoint):
        def get(self) -> HTTPBinResponse:
            return self._get("/get", response_model=HTTPBinResponse)

    class HTTPBinClient(APIClient):
        _base_url = "https://httpbin.org"

        methods: MethodsAPI

So now if we use the client like before, what will be returned is an HTTPBinResponse object with the JSON payload from
the response un-marshaled into it.

.. code:: python
    :number-lines:

    client = HTTPBinClient()
    resp = client.methods.get()
    print(f"We called HTTPBin from {resp.origin}")
    # Prints: We called HTTPBin from 1.2.3.4

We can also leverage the concrete list type as well if we expect to see an array of objects being returned. For example
the follow if valid:

.. code:: python
    :number-lines:

    class Item(BaseModel):
        id: int
        name: str


    class ItemsAPI(APIEndpoint):
        _path = "/items"

        def list(self) -> list[Item]:
            return self._get("", response_model=list[Item])


    class ExampleClient(APIClient):
        _base_url = "https://example.com"

        items: ItemsAPI


    # Running it!
    example = ExampleClient()
    for item in example.items.list():
        print(f"{item.id} is named {item.name}")


What about XML Responses?
^^^^^^^^^^^^^^^^^^^^^^^^^

XML data is handled using the Pydantic-XML library and can be used the same way. Using HTTPBin's XML example endpoint
as a basis, we would write this:

.. code:: python
    :number-lines:

    from pydantic_xml import BaseXmlModel

    class XmlSlide(BaseXmlModel, tag="slide"):
        title: str = element()
        items: list[str] = element(tag="item", default=None)


    class XmlSlideshow(BaseXmlModel, tag="slideshow"):
        title: str = attr()
        date: str = attr()
        author: str = attr()
        slides: list[XmlSlide] = element(tag="slide", default=None)


    class FormatAPI(APIEndpoint):
        def xml(self) -> XmlSlideshow:
            return self._get("/xml", response_model=XmlSlideshow)

Pagination
----------

Most APIs will break up larger datasets into multiple calls or "pages" of data in some way, shape, or form. Depending
on the API, this can be handled through anything from simple page iterators, offsets, next ids, scroll ids,
asynchronous jobs, etc. Regardless of the mechanism, the goal is simply to "collect all the data" with some
control over things like call volume, memory size, number of elements, etc. Many times, this leaves developers with
having to call each page, work on the available elements, and then call the next, and so on. Typically this means that
with something like the following implementation,

.. code:: python
    :number-lines:

    class Item(BaseModel):
        id: int
        name: str

    class ExampleAPI(APIEndpoint):
        _path = "/items"

        def page(self, page: int = 0, size: int = 100) -> list[Item]:
            return self._get("", params={"page": page, "size": size}, response_model=list[Item])

    class ExampleClient(APIClient):
        _base_url = "https://example.org"
        items: ExampleAPI

Now to use something like that, the caller has to know how to handle the pages and when to call the next, so in the
case of this API that simply returns a list of items back, its up to the caller to know that when a page isn't equal
to the size, that it's the last page:

.. code:: python
    :number-lines:

    client = ExampleClient()

    pages = 0
    size = 100
    items: list[Item]
    while len(items) >= size or pages == 0:
        items = client.items.page(page=pages, size=size)
        for item in items:
            ...

If this pattern is always expected, and should always be followed, when instead of having the developer write this
out every single time, we can always centralize this logic within the library.  There are two approaches that can be
used here depending on amount of control desired.

Generators
^^^^^^^^^^

Building a generator to vendor that exact logic is really simple! IN the example below, we simply added a new method
that behaves like a generator instead of returning the page directly.

.. code:: python
    :number-lines:

    class ExampleAPI(APIEndpoint):
        def list(self, size: int = 100, page: int = 0) -> Generator[Item, None, None]:
            items: list[Item]
            while len(items) >= size or pages == 0:
                items = self.page(page=page, size=size)
                page += 1
                for item in items:
                    yield item

Then to use it, all you need to do is:

.. code:: python
    :number-lines:

    for item in client.items.list():
        print(item)

Obviously there are multiple other avenues that can be taken to approach generators, however methods similar to this
one are the simplest.

Iterators
^^^^^^^^^

While generators are incredibly powerful and make handling things like pagination incredibly easy, there are some
limitations that need to be understood. As a generator itself can't expose any additional attributes, it would mean
that some more complex tasks may be more difficult with them. There can also be the issue of exposing job ids or other
attributes that may be needed for later use. In order to get around that, there is also an ``APIIterator``
(and associated ``AsyncAPIIterator``) class that you can use as a base if you desire to expose more to the caller.

Using the same example as above, lets instead make an iterator:

.. code:: python
    :number-lines:

    from restfly import APIIterator

    class ItemsIterator(APIIterator):
        size: int = 100
        current_page: int = 0

        def _get_page(self):
            resp = self._client.items.page(page=self.current_page, size=self.size)
            self.page = resp

    class ExampleAPI(APIEndpoint):
        def list(self, size: int = 100, page: int = 0) -> ItemsIterator:
            return ItemsIterator(client=self._client, size=size, current_page=page)

And then to use it, you just need to do:

.. code:: python
    :number-lines:

    for item in client.items.list():
        print(item)

However you can also now store the iterator and call the different components or attributes:

.. code:: python
    :number-lines:

    items = client.items.list()
    print(items.current_page)
    item = next(items)
    print(item)
    print(items.page)

.. note::
    By default the APIIterator object wont make any API calls until the first element is requested. This is done
    this way to get the iterator to return back to the caller as quickly as possible.

The APIIterator class has enough of the basic pagination logic baked in to typically not need to do a whole lot,
(typically just overloading the `_get_page` method with your retrieval logic) however can be overloaded in a multitude
of different ways if necessary.  If you're looking to augment or extend the APIIterator, please take a look at the
reference guide and the APIIterator source to understand what already exists for you.

Authentication
--------------

Here are some examples based on what is mocked in the `HTTPX documentation`_.  As you may have noticed, RESTFly will
typically pass through any parameters that are known into the HTTPX Client, so any adapters that may be needed should
typically directly work.

.. _HTTPX documentation: https://www.python-httpx.org/advanced/authentication/


Basic Auth
^^^^^^^^^^

.. code:: python
    :number-lines:

    from httpx import BasicAuth

    class ExampleClient(APIClient):
        _base_url = "https://example.com"

        def __init__(self, username: str, password: str):
            super().__init__(auth=BasicAuth(username=username, password=password))

        def _deauthenticate(self):
            """ Logs the user out with a DELETE /token API Call """
            self._delete("/token")


Digest Auth
^^^^^^^^^^^

.. code:: python
    :number-lines:

    from httpx import DigestAuth

    class ExampleClient(APIClient):
        _base_url = "https://example.com"

        def __init__(self, username: str, password: str):
            super().__init__(auth=DigestAuth(username=username, password=password))

        def _deauthenticate(self):
            """ Logs the user out with a DELETE /token API Call """
            self._delete("/token")


Custom Auth (API Keys)
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python
    :number-lines:

    class ExampleClient(APIClient):
        _base_url = "https://example.com"

        def __init__(self, api_key: str):
            super().__init__(headers={"X-API-Key": api_key})

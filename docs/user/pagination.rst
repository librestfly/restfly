.. _pagination:

Pagination
==========

.. image:: https://live.staticflickr.com/3620/3314919669_c4a8aaa604_b.jpg

Typically when an API has a larger volume of data, it's common to break that dataset up
into manageable "pages" of data.  Depending on the API, this can be handled any number
of different ways, however the overall theme is is the same: Collect X number of objects
in a request, then collect the next X number, then the next, and so on.  When you look
at how this looks from an API perspective, this would end up looking something similar
to below:

    >>> api = ExampleAPI()
    >>> page = api.get('items', params={'page': 1, 'size': 10})
    >>> next_page = api.get('items', params={'page': 2, 'size': 10})
    >>> next_next = api.get('items', params={'page': 3, 'size': 10})

While this works just fine, it does require the developer to know how to handle the
pagination, know the limits of the API, and how to burn down each page of data.  For
some folks this may be perfectly fine, however with a little effort we can turn these
series of calls into an iterator that handles those page calls for the developer and
allows the developer to use this paginated API within a simple for loop.  RESTfly has a
basic iterator already setup with most of the pagination logic already written.  All we
need to do is override the _get_page method with the actual calls.  For this example, we
will assume that the items are enclosed in an items attribute and that there is a total
attribute:

.. code-block:: json

    {
        "items": [
            {"id": 1},
            {"id": 2},
            {"id": 3}
        ],
        "total": 101
    }

To wrap that response in an iterator, all we need to do tell the iterator how to handle
the pagination of the responses:

    >>> from restfly.iterator import APIIterator
    >>> class ItemIterator(APIIterator):
    ...     page_size: int = 10
    ...
    ...     def _get_page(self) -> None:
    ...         """
    ...         Gets the next page of data
    ...         """
    ...         resp = self._api.get('items', params={
    ...             'page': self.num_pages + 1,
    ...             'size': self.page_size
    ...         }).json()
    ...         # get the total and the items list from the response and store them into
    ...         # the reserved attributes.
    ...         self.total = resp.get('total')
    ...         self.page = resp.get('items', [])

Alright, so we have an iterator class now, but how to we use it?  To start, we
should manually test it and see how it works:

    >>> items = ItemIterator(api, page_size=10)
    >>> for item in items:
    ...     print(item)

We should see the items being fed to the for loop through the iterator.  Once the total
number of records has been reached (regardless of how many pages), the iterator will
terminate with a ``StopIteration`` exception.

Now, lets go ahead and wire this into an endpoint method:

    >>> from restfly.endpoint import APIEndpoint
    >>> class ItemsEndpoint(APIEndpoint):
    ...     def list(
    ...         self,
    ...         page_size: int = 10,
    ...         max_items: Optional[int] = None,
    ...         max_pages: Optional[int] = None,
    ...     ) -> ItemIterator:
    ...         return ItemIterator(
    ...             self._api,
    ...             page_size=page_size,
    ...             max_items=max_items,
    ...             max_pages=max_pages
    ...         )
    ...

So now, once we wire it into the ExampleAPI class like so:

    >>> class ExampleAPI(APISession):
    ...     @property
    ...     def items(self) -> ItemsEndpoint:
    ...         return ItemsEndpoint(self)

We now can simply call the items.list method and get the iterator returned back
to us.  This allows for us to call the ``items.list`` method and loop over it without
any care as to how the underlying pagination is being handled.

    >>> api = ExampleAPI()
    >>> for item in api.items.list():
    ...     print(item)

from __future__ import annotations

import logging
from typing import Any, Self

from ._async import AsyncAPIClient
from ._sync import APIClient


class APIIterator:
    """
    The API iterator provides a scalable way to work through result sets of any
    size.  The iterator will walk through each page of data, returning one
    record at a time.  If it reaches the end of a page of records, then it will
    request the next page of information and then continue to return records
    from the next page (and the next, and the next) until the counter reaches
    the total number of records that the API has reported.

    Note that this Iterator is used as a base model for all of the iterators,
    and while the mechanics of each iterator may vary, they should all behave
    to the user in a similar manner.
    """

    count: int = 0
    """ Current count of objects that have been returned. """

    page_count: int = 0
    """ Current count of objects from the current page that have been returned. """

    num_pages: int = 0
    """ The number of pages that have been requested. """

    max_pages: int | None = None
    """ The maximum number of pages to request before terminating. """

    max_items: int | None = None
    """ The maximum number of objects to return before terminating. """

    total: int | None = None
    """ The total number of objects that could be returned. """

    page: list[Any]
    """ The current page of data. """

    _client: APIClient
    """ The API Client object to use for calling the API. """

    def __init__(self, client: APIClient, **kw):
        """
        Args:
            api (restfly.session.APISession):
                The APISession object to use for this iterator.
            **kw (dict):
                The various attributes to add/overload in the iterator.

        Example:
            >>> i = APIIterator(api, max_pages=1, max_items=100)
        """
        self._client = client
        self.__dict__.update(kw)
        self.page = []

        # Create the logging facility
        self._log = logging.getLogger(__name__)

    def __getitem__(self, key: int) -> Any:
        return self.page[key]

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Any:
        """
        Ask for the next record
        """
        # If there are no more records to return, then we should raise a
        # StopIteration exception to break the iterator out.
        if (self.total and self.count >= self.total) or (
            self.max_items and self.count >= self.max_items
        ):
            raise StopIteration()

        # If we have worked through the current page of records and we still
        # haven't hit to the total number of available records, then we should
        # query the next page of records.
        if self.page_count >= len(self.page) and (
            not self.total or self.count + 1 <= self.total
        ):
            # If the number of pages requested reaches the total number of
            # pages that should be requested, then stop iteration.
            if self.max_pages and self.num_pages + 1 > self.max_pages:
                raise StopIteration()

            # Perform the _get_page call.
            self._get_page()
            self.page_count = 0
            self.num_pages += 1

            # If the length of the page is 0, then we don't have anything
            # further to do and should stop iteration.
            if len(self.page) == 0:
                raise StopIteration()

        # Get the relevant record, increment the counters, and return the
        # record.
        item = self._get_next_item()
        self._increment_counters()
        return item

    def _increment_counters(self) -> None:
        """
        Handles incrementing all of the counters that are controlling the next item
        to be retrieved.
        """
        self.count += 1
        self.page_count += 1

    def _get_next_item(self) -> Any:
        """
        Returns the next item in the page
        """
        return self[self.page_count]

    def _get_page(self) -> None:
        """
        A method to be overloaded in order to instruct the iterator how to
        retrieve the next page of data.

        Example:
            >>> class ExampleIterator(APIIterator):
            ...    def _get_page(self):
            ...        self.total = 100
            ...        items = range(10)
            ...        self.page = [{'id': i + self._offset} for i in items]
            ...        self._offset += self._limit
        """

    def get(self, key: int, default: Any | None = None) -> Any:
        """
        Retrieves an item from the the current page based off of the key.

        Args:
            key (int): The index of the item to retrieve.
            default (obj): The returned object if the item does not exist.

        Examples:
            >>> a = APIIterator()
            >>> a.get(2)
            None
        """
        try:
            return self[key]
        except IndexError:
            return default


class AsyncAPIIterator:
    """
    The API iterator provides a scalable way to work through result sets of any
    size.  The iterator will walk through each page of data, returning one
    record at a time.  If it reaches the end of a page of records, then it will
    request the next page of information and then continue to return records
    from the next page (and the next, and the next) until the counter reaches
    the total number of records that the API has reported.

    Note that this Iterator is used as a base model for all of the iterators,
    and while the mechanics of each iterator may vary, they should all behave
    to the user in a similar manner.
    """

    count: int = 0
    """ Current count of objects that have been returned. """

    page_count: int = 0
    """ Current count of objects from the current page that have been returned. """

    num_pages: int = 0
    """ The number of pages that have been requested. """

    max_pages: int | None = None
    """ The maximum number of pages to request before terminating. """

    max_items: int | None = None
    """ The maximum number of objects to return before terminating. """

    total: int | None = None
    """ The total number of objects that could be returned. """

    page: list[Any]
    """ The current page of data. """

    _client: AsyncAPIClient
    """ The API Client object to use for calling the API. """

    def __init__(self, client: AsyncAPIClient, **kw):
        """
        Args:
            api (restfly.session.APISession):
                The APISession object to use for this iterator.
            **kw (dict):
                The various attributes to add/overload in the iterator.

        Example:
            >>> i = APIIterator(api, max_pages=1, max_items=100)
        """
        self._client = client
        self.__dict__.update(kw)
        self.page = []

        # Create the logging facility
        self._log = logging.getLogger(__name__)

    def __getitem__(self, key: int) -> Any:
        return self.page[key]

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> Any:
        """
        Ask for the next record
        """
        # If there are no more records to return, then we should raise a
        # StopIteration exception to break the iterator out.
        if (self.total and self.count >= self.total) or (
            self.max_items and self.count >= self.max_items
        ):
            raise StopAsyncIteration()

        # If we have worked through the current page of records and we still
        # haven't hit to the total number of available records, then we should
        # query the next page of records.
        if self.page_count >= len(self.page) and (
            not self.total or self.count + 1 <= self.total
        ):
            # If the number of pages requested reaches the total number of
            # pages that should be requested, then stop iteration.
            if self.max_pages and self.num_pages + 1 > self.max_pages:
                raise StopAsyncIteration()

            # Perform the _get_page call.
            await self._get_page()
            self.page_count = 0
            self.num_pages += 1

            # If the length of the page is 0, then we don't have anything
            # further to do and should stop iteration.
            if len(self.page) == 0:
                raise StopAsyncIteration()

        # Get the relevant record, increment the counters, and return the
        # record.
        item = self._get_next_item()
        self._increment_counters()
        return item

    def _increment_counters(self) -> None:
        """
        Handles incrementing all of the counters that are controlling the next item
        to be retrieved.
        """
        self.count += 1
        self.page_count += 1

    def _get_next_item(self) -> Any:
        """
        Returns the next item in the page
        """
        return self[self.page_count]

    async def _get_page(self) -> None:
        """
        A method to be overloaded in order to instruct the iterator how to
        retrieve the next page of data.

        Example:
            >>> class ExampleIterator(APIIterator):
            ...    def _get_page(self):
            ...        self.total = 100
            ...        items = range(10)
            ...        self.page = [{'id': i + self._offset} for i in items]
            ...        self._offset += self._limit
        """

    async def get(self, key: int, default: Any | None = None) -> Any:
        """
        Retrieves an item from the the current page based off of the key.

        Args:
            key (int): The index of the item to retrieve.
            default (obj): The returned object if the item does not exist.

        Examples:
            >>> a = APIIterator()
            >>> a.get(2)
            None
        """
        try:
            return self[key]
        except IndexError:
            return default

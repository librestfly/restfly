'''
.. autoclass:: APIIterator
'''


class APIIterator(object):
    '''
    The API iterator provides a scalable way to work through result sets of any
    size.  The iterator will walk through each page of data, returning one
    record at a time.  If it reaches the end of a page of records, then it will
    request the next page of information and then continue to return records
    from the next page (and the next, and the next) until the counter reaches
    the total number of records that the API has reported.

    Note that this Iterator is used as a base model for all of the iterators,
    and while the mechanics of each iterator may vary, they should all behave
    to the user in a similar manner.

    Attributes:
        count (int): The current number of records that have been returned
        page (list):
            The current page of data being walked through.  pages will be
            cycled through as the iterator requests more information from the
            API.
        page_count (int): The number of record returned from the current page.
        total (int):
            The total number of records that exist for the current request.
    '''
    count = 0
    page_count = 0
    num_pages = 0
    max_pages = None
    max_items = None
    total = None
    page = []

    # The API will be grafted on here.
    _api = None

    # The page size limit
    _limit = None

    # The current record offset
    _offset = 0

    def __init__(self, api, **kw):
        self._api = api
        self.__dict__.update(kw)

    def _get_page(self):
        pass

    def get(self, index, default=None):
        '''
        Retrieves an item from the the current page based off the index provided.

        Args:
            index (int): The index of the item to retrieve.
            default
        '''
        try:
            return self.page[int(index)]
        except IndexError:
            return default

    def __getitem__(self, key):
        return self.page[key]

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        '''
        Ask for the next record
        '''
        # If there are no more records to return, then we should raise a
        # StopIteration exception to break the iterator out.
        if ((self.total and self.count + 1 > self.total)
          or (self.max_items and self.count + 1 > self.max_items)
          or (self.max_pages and self.num_pages > self.max_pages)):
            raise StopIteration()

        # If we have worked through the current page of records and we still
        # haven't hit to the total number of available records, then we should
        # query the next page of records.
        if (self.page_count >= len(self.page)
          and (not self.total or self.count + 1 <= self.total)):

            # If the number of pages requested reaches the total number of pages
            # that should be requested, then stop iteration.
            if self.max_pages and self.num_pages + 1 > self.max_pages:
                raise StopIteration()

            # Perform the _get_page call.
            self.page_count = 0
            self.num_pages += 1
            self._get_page()

            # If the length of the page is 0, then we don't have anything
            # further to do and should stop iteration.
            if len(self.page) == 0:
                raise StopIteration()

        # Get the relevant record, increment the counters, and return the
        # record.
        self.count += 1
        self.page_count += 1
        item = self[self.page_count - 1]
        return item
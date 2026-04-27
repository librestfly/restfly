import pytest
from restfly import APIIterator, AsyncAPIIterator


class ExampleIterator(APIIterator):
    limit = 10
    offset = 0

    def _get_page(self):
        self.total = 100
        self.page = [{"id": i + self.offset} for i in range(self.limit)]
        self.offset += self.limit


class AsyncExampleIterator(AsyncAPIIterator):
    limit = 10
    offset = 0

    async def _get_page(self):
        self.total = 100
        self.page = [{"id": i + self.offset} for i in range(self.limit)]
        self.offset += self.limit


def test_iterator_stubs():
    assert APIIterator(None)._get_page() is None  # ty: ignore[invalid-argument-type]


def test_iterator_get_key():
    items = ExampleIterator(None)  # ty: ignore[invalid-argument-type]
    next(items)
    assert items.get(0) == {"id": 0}
    assert items[0] == {"id": 0}
    assert items.get(101, None) is None


def test_blank_page():
    class ExIterator(APIIterator): ...

    with pytest.raises(StopIteration):
        next(ExIterator(None))  # ty: ignore[invalid-argument-type]


def test_iterator():
    items = ExampleIterator(None)  # ty: ignore[invalid-argument-type]
    last_item = None
    for item in items:
        last_item = item
    assert last_item == {"id": 99}
    assert items.total == 100
    assert items.count == 100
    assert items.num_pages == 10
    assert items.page_count == 10
    assert items.page == [
        {"id": 90},
        {"id": 91},
        {"id": 92},
        {"id": 93},
        {"id": 94},
        {"id": 95},
        {"id": 96},
        {"id": 97},
        {"id": 98},
        {"id": 99},
    ]


def test_iterator_max_items():
    items = ExampleIterator(None, max_items=15)  # ty: ignore[invalid-argument-type]
    last_item = None
    for item in items:
        last_item = item
    assert last_item == {"id": 14}
    assert items.total == 100
    assert items.count == 15
    assert items.num_pages == 2
    assert items.page_count == 5
    assert items.page == [
        {"id": 10},
        {"id": 11},
        {"id": 12},
        {"id": 13},
        {"id": 14},
        {"id": 15},
        {"id": 16},
        {"id": 17},
        {"id": 18},
        {"id": 19},
    ]


def test_iterator_max_pages():
    items = ExampleIterator(None, max_pages=2)  # ty: ignore[invalid-argument-type]
    last_item = None
    for item in items:
        last_item = item
    assert last_item == {"id": 19}
    assert items.total == 100
    assert items.count == 20
    assert items.num_pages == 2
    assert items.page_count == 10
    assert items.page == [
        {"id": 10},
        {"id": 11},
        {"id": 12},
        {"id": 13},
        {"id": 14},
        {"id": 15},
        {"id": 16},
        {"id": 17},
        {"id": 18},
        {"id": 19},
    ]


async def test_async_iterator_stubs():
    assert await AsyncAPIIterator(None)._get_page() is None  # ty: ignore[invalid-argument-type]


async def test_async_iterator_get_key():
    items = AsyncExampleIterator(None)  # ty: ignore[invalid-argument-type]
    await anext(items)
    assert await items.get(0) == {"id": 0}
    assert items[0] == {"id": 0}
    assert await items.get(101, None) is None


async def test_async_blank_page():
    class AsyncExIterator(AsyncAPIIterator): ...

    with pytest.raises(StopAsyncIteration):
        await anext(AsyncExIterator(None))  # ty: ignore[invalid-argument-type]


async def test_async_iterator():
    items = AsyncExampleIterator(None)  # ty: ignore[invalid-argument-type]
    last_item = None
    async for item in items:
        last_item = item
    assert last_item == {"id": 99}
    assert items.total == 100
    assert items.count == 100
    assert items.num_pages == 10
    assert items.page_count == 10
    assert items.page == [
        {"id": 90},
        {"id": 91},
        {"id": 92},
        {"id": 93},
        {"id": 94},
        {"id": 95},
        {"id": 96},
        {"id": 97},
        {"id": 98},
        {"id": 99},
    ]


async def test_asynciterator_max_items():
    items = AsyncExampleIterator(None, max_items=15)  # ty: ignore[invalid-argument-type]
    last_item = None
    async for item in items:
        last_item = item
    assert last_item == {"id": 14}
    assert items.total == 100
    assert items.count == 15
    assert items.num_pages == 2
    assert items.page_count == 5
    assert items.page == [
        {"id": 10},
        {"id": 11},
        {"id": 12},
        {"id": 13},
        {"id": 14},
        {"id": 15},
        {"id": 16},
        {"id": 17},
        {"id": 18},
        {"id": 19},
    ]


async def test_async_iterator_max_pages():
    items = AsyncExampleIterator(None, max_pages=2)  # ty: ignore[invalid-argument-type]
    last_item = None
    async for item in items:
        last_item = item
    assert last_item == {"id": 19}
    assert items.total == 100
    assert items.count == 20
    assert items.num_pages == 2
    assert items.page_count == 10
    assert items.page == [
        {"id": 10},
        {"id": 11},
        {"id": 12},
        {"id": 13},
        {"id": 14},
        {"id": 15},
        {"id": 16},
        {"id": 17},
        {"id": 18},
        {"id": 19},
    ]

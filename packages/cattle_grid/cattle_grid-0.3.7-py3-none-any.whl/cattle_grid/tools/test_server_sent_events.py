import asyncio

from .server_sent_events import async_iterator_for_queue_and_task


async def test_async_iterator_for_queue_and_task_stops_on_None():
    queue = asyncio.Queue()

    async def task_function():
        await queue.put(None)
        await asyncio.sleep(60)

    task = asyncio.create_task(task_function())

    iterator = async_iterator_for_queue_and_task(queue, task)

    async for _ in iterator:
        ...


async def test_async_iterator_for_queue_and_task_iterators():
    queue = asyncio.Queue()
    for x in ["one", "two", "three", None]:
        await queue.put(x)

    async def task_function(): ...

    task = asyncio.create_task(task_function())

    iterator = async_iterator_for_queue_and_task(queue, task)

    results = []

    async for x in iterator:
        results.append(x)

    assert results == ["one", "two", "three"]

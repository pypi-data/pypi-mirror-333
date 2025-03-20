from unittest.mock import AsyncMock, MagicMock
from contextlib import asynccontextmanager
from asyncstdlib.itertools import islice

from cattle_grid.model.account import EventType

from .streaming import get_message_streamer


async def test_get_message_streamer():
    broker = MagicMock()

    @asynccontextmanager
    async def connection():
        yield AsyncMock()

    broker._connection = connection()

    streamer = get_message_streamer(AsyncMock(), 0.1)

    count = 0
    count_target = 3

    async for x in islice(streamer("account-name", MagicMock(EventType)), count_target):
        count = count + 1

    assert count == count_target

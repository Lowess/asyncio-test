import asyncio
from aiohttp import ClientSession
import pytest
from async_req import Async
import logging

logger = logging.getLogger(__name__)

from asyncmock import AsyncMock


class MockResponse(AsyncMock):
    @property
    def headers(self):
        return {"content-type": "application/json"}

    async def json(self):
        return {"hello": "world"}


async def _await_none(x):
    """Mock backoff to not sleep"""
    return None


class TestAsync:
    @pytest.mark.asyncio
    async def test_async(
        self,
        monkeypatch,
    ):
        cli = Async()
        cli._fetch = MockResponse()

        async with ClientSession() as session:
            with monkeypatch.context() as m:
                # Patch asyncio.sleep used by backoff.on_exception to speed up exec
                m.setattr(asyncio, "sleep", _await_none)

                url_response = await cli.call("http://example.com", session=session)
                logger.info(url_response)

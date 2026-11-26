import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

from app.application import close_router


def test_cleanup_continues_after_one_provider_fails():
    first = AsyncMock(side_effect=RuntimeError("cleanup failed"))
    second = AsyncMock()
    router = SimpleNamespace(providers={
        "first": SimpleNamespace(close=first), "second": SimpleNamespace(close=second),
    })
    asyncio.run(close_router(router))
    first.assert_awaited_once()
    second.assert_awaited_once()

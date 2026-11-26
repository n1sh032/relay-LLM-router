import asyncio

import httpx
import pytest

import main
from app.providers.base import ChatResponse, IncompleteResponseError
from app.routing.router import Router


def post(request):
    async def send():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=main.app), base_url="http://test",
        ) as client:
            return await client.post("/chat", json=request)

    return asyncio.run(send())


@pytest.mark.parametrize("change", [
    {"messages": [{"role": "tool", "content": "x"}]},
    {"messages": [{"role": "user", "content": "x" * 16001}]},
    {"temperature": 3},
    {"max_tokens": 0},
    {"quality": "unknown"},
])
def test_invalid_request(change):
    request = {"messages": [{"role": "user", "content": "hello"}]}
    assert post(request | change).status_code == 422

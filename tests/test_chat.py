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

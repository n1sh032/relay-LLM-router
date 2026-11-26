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


def test_request_body_size_is_limited():
    request = {"messages": [{"role": "user", "content": "x" * (512 * 1024)}]}
    assert post(request).status_code == 413
def test_fallback_and_errors(monkeypatch):
    class Empty:
        async def chat(self, request):
            raise IncompleteResponseError()

    class Working:
        async def chat(self, request):
            return ChatResponse(content="hello", model=request.model, provider="gemini",
                                input_tokens=None, output_tokens=None)

    request = {"messages": [{"role": "user", "content": "hello"}]}
    for providers, status in [
        ({}, 503),
        ({"openai": Empty()}, 502),
        ({"openai": Empty(), "gemini": Working()}, 200),
    ]:
        monkeypatch.setattr(main, "router", Router(providers))
        response = post(request)
        assert response.status_code == status
    assert response.json()["provider"] == "gemini"

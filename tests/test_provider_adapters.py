import asyncio
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock

import pytest

from app.providers.base import IncompleteResponseError, ProviderRequest
from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider


def request():
    return ProviderRequest(
        model="test-model",
        messages=[
            {"role": "system", "content": "Keep it brief."},
            {"role": "user", "content": "Hello."},
        ],
    )


def test_openai_preserves_length_finish_reason_and_missing_usage():
    create = AsyncMock(return_value=NS(choices=[
        NS(message=NS(content="Partial reply"), finish_reason="length"),
    ]))
    provider = OpenAIProvider.__new__(OpenAIProvider)
    provider.client = NS(chat=NS(completions=NS(create=create)))
    response = asyncio.run(provider.chat(request()))
    assert response.finish_reason == "length"
    assert response.input_tokens is None
    assert response.model == "test-model"

    create.return_value = NS(choices=[])
    with pytest.raises(IncompleteResponseError):
        asyncio.run(provider.chat(request()))


def test_gemini_sends_system_message_separately():
    generate = AsyncMock(return_value=NS(text="Hello", candidates=[NS(finish_reason="MAX_TOKENS")]))
    provider = GeminiProvider.__new__(GeminiProvider)
    provider.client = NS(aio=NS(models=NS(generate_content=generate)))
    response = asyncio.run(provider.chat(request()))

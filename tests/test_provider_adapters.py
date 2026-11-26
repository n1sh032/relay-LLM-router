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

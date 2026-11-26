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



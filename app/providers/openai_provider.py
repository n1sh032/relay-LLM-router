import os
from openai import AsyncOpenAI
from app.providers.base import Provider, ChatRequest, ChatResponse


class OpenAIProvider(Provider):

    def __init__(self):
        # grabs the key from env vars, never hardcode this stuff
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def chat(self, request: ChatRequest) -> ChatResponse:
        # openai wants messages as plain dicts, not our pydantic objects
        # so gotta convert first
        openai_messages = [
            {"role": m.role, "content": m.content} for m in request.messages
        ]


import os
from openai import AsyncOpenAI
from app.providers.base import Provider, ChatRequest, ChatResponse


class OpenAIProvider(Provider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def chat(self, request: ChatRequest) -> ChatResponse:
        # openai wants plain dicts not pydantic objects
        openai_messages = [{"role": m.role, "content": m.content} for m in request.messages]

        response = await self.client.chat.completions.create(
            model=request.model,
            messages=openai_messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        choice = response.choices[0]
        # putting their response back into my format
        return ChatResponse(
            content=choice.message.content,
            provider="openai",
            model=response.model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
        )
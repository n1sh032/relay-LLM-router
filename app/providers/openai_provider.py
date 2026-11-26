import os
from openai import AsyncOpenAI
from app.providers.base import Provider, ProviderRequest, ChatResponse, IncompleteResponseError


class OpenAIProvider(Provider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=0, timeout=30)

    async def chat(self, request: ChatRequest) -> ChatResponse:
        # openai wants plain dicts not pydantic objects
        openai_messages = [{"role": m.role, "content": m.content} for m in request.messages]

        response = await self.client.chat.completions.create(
            model=request.model,
            messages=openai_messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        choices = getattr(response, "choices", None)
        content = getattr(getattr(choices[0], "message", None), "content", None) if choices else None
        if not isinstance(content, str) or not content.strip():
            raise IncompleteResponseError()
        usage = getattr(response, "usage", None)
        # putting their response back into my format
        return ChatResponse(
            content=content,
            provider="openai",
            model=getattr(response, "model", None) or request.model,
            input_tokens=getattr(usage, "prompt_tokens", None),
            output_tokens=getattr(usage, "completion_tokens", None),
        )

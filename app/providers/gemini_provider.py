import os
from google import genai
from app.providers.base import Provider, ChatRequest, ChatResponse, IncompleteResponseError


class GeminiProvider(Provider):
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    async def chat(self, request: ChatRequest) -> ChatResponse:
        # gemini uses "model" instead of "assistant" for role, annoying
        # spent way too long debugging this before i realised
        gemini_messages = []
        config = {"max_output_tokens": request.max_tokens, "temperature": request.temperature}
        for m in request.messages:
            if m.role == "system":
                config["system_instruction"] = m.content
                continue
            role = "model" if m.role == "assistant" else m.role
            gemini_messages.append({"role": role, "parts": [{"text": m.content}]})

        response = await self.client.aio.models.generate_content(
            model=request.model,
            contents=gemini_messages,
            config=config,
        )

        content = getattr(response, "text", None)
        if not isinstance(content, str) or not content.strip():
            raise IncompleteResponseError()
        usage = getattr(response, "usage_metadata", None)
        return ChatResponse(
            content=content,
            provider="gemini",
            model=request.model,
            input_tokens=getattr(usage, "prompt_token_count", None),
            output_tokens=getattr(usage, "candidates_token_count", None),
        )

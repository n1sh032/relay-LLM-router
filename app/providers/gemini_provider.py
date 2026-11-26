import os
from google import genai
from app.providers.base import Provider, ChatRequest, ChatResponse

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiProvider(Provider):
    async def chat(self, request: ChatRequest) -> ChatResponse:
        # gemini uses "model" instead of "assistant" for role, annoying
        # spent way too long debugging this before i realised
        gemini_messages = []
        for m in request.messages:
            role = "model" if m.role == "assistant" else m.role
            gemini_messages.append({"role": role, "parts": [{"text": m.content}]})

        response = await client.aio.models.generate_content(
            model=request.model,
            contents=gemini_messages,
            config={
                "max_output_tokens": request.max_tokens,
                "temperature": request.temperature,
            },
        )

        return ChatResponse(
            content=response.text,
            provider="gemini",
            model=request.model,
            input_tokens=response.usage_metadata.prompt_token_count,
            output_tokens=response.usage_metadata.candidates_token_count,
        )
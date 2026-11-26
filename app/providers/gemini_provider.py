import os
from google import genai
from app.providers.base import Provider, ChatRequest, ChatResponse

# new sdk uses a client object instead of the old configure() global setup
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiProvider(Provider):

    async def chat(self, request: ChatRequest) -> ChatResponse:
        # gemini doesnt use "assistant" as a role like openai does
        # it wants "model" instead, learned this the hard way earlier
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

        # gemini gives token counts in a different spot than openai does
        usage = response.usage_metadata

        return ChatResponse(
            content=response.text,
            provider="gemini",
            model=request.model,
            input_tokens=usage.prompt_token_count,
            output_tokens=usage.candidates_token_count,
        )
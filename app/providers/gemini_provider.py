import os
from google import genai
from app.providers.base import Provider, ChatRequest, ChatResponse

# new sdk uses a client object instead of the old configure() global setup
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiProvider(Provider):

    async def chat(self, request: ChatRequest) -> ChatResponse:
        model = genai.GenerativeModel(request.model)

        # gemini doesnt use "assistant" as a role, it wants "model" instead
        # so gotta remap that or it just errors out (learned this the hard way)
        gemini_messages = []
        for m in request.messages:
            role = "model" if m.role == "assistant" else m.role
            gemini_messages.append({"role": role, "parts": [m.content]})

        response = await model.generate_content_async(
            gemini_messages,
            generation_config={
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
import os
import google.generativeai as genai
from app.providers.base import Provider, ChatRequest, ChatResponse

# gemini needs to be configured globally with the key first
# before you can even create a model object, kinda annoying
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiProvider(Provider):

    async def chat(self, request: ChatRequest) -> ChatResponse:
        model = genai.GenerativeModel(request.model)

        # gemini doesnt use "assistant" as a role, it wants "model" instead

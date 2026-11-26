from openai import APIError as OpenAIAPIError
from google.genai.errors import APIError as GeminiAPIError
from app.providers.base import Provider, ChatRequest, ChatResponse


class AllProvidersFailedError(Exception):
    pass


# which provider + model to try for each quality level
# ordered by preference, first one gets tried first
MODEL_MAP = {
    "fast": [
        ("openai", "gpt-4o-mini"),
        ("gemini", "gemini-2.5-flash"),
    ],
    "smart": [
        ("openai", "gpt-4o"),
        ("gemini", "gemini-2.5-pro"),
    ],
}

# only fall back for actual provider errors, not bugs in my own code
PROVIDER_ERRORS = (OpenAIAPIError, GeminiAPIError)


class Router:
    def __init__(self, providers: dict[str, Provider]):
        self.providers = providers

    async def chat(self, request: ChatRequest) -> ChatResponse:
        options = MODEL_MAP.get(request.quality, MODEL_MAP["fast"])
        last_error = None

        for provider_name, model_name in options:
            provider = self.providers[provider_name]
            provider_request = request.model_copy(update={"model": model_name})

            try:
                return await provider.chat(provider_request)
            except PROVIDER_ERRORS as e:
                print(f"{provider_name} failed: {e}")
                last_error = e
                continue
            # anything else isnt caught here on purpose, i want real bugs to crash

        raise AllProvidersFailedError(f"all providers failed. last error: {last_error}")
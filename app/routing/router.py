from openai import APIError as OpenAIAPIError
from google.genai.errors import APIError as GeminiAPIError
from app.providers.base import Provider, ChatRequest, ChatResponse


class AllProvidersFailedError(Exception):
    pass


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

# only these count as "provider failed, try the next one"
# anything else (like a bug in my own code) should crash loudly instead
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
                # actual provider failure - openai/gemini rejected us,
                # network issue, etc - fine to fall back
                print(f"{provider_name} failed: {e}")
                last_error = e
                continue
            # anything NOT in PROVIDER_ERRORS (bugs, typos, etc)
            # will crash normally instead of being hidden here

        raise AllProvidersFailedError(f"all providers failed, last error: {last_error}")
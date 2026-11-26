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
        # dict this time so i can look up "openai" -> its provider object
        self.providers = providers

    async def chat(self, request: ChatRequest) -> ChatResponse:
        options = MODEL_MAP.get(request.quality, MODEL_MAP["fast"])

        last_error = None

        for provider_name, model_name in options:
            provider = self.providers[provider_name]

            # each provider gets told exactly which model to use for THIS
            # attempt instead of relying on whatever the caller sent
            provider_request = request.model_copy(update={"model": model_name})

            try:
                return await provider.chat(provider_request)
            except Exception as e:
                # for now just catching everything and moving to the next
                # provider. will make this smarter later - some errors
                # shouldnt even trigger a fallback (like a bad request)
                print(f"{provider_name} failed: {e}")
                last_error = e
                continue

        # if we get here, literally nothing worked
        raise AllProvidersFailedError(f"all providers failed, last error: {last_error}")
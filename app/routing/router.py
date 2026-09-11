from app.providers.base import Provider, ChatRequest, ChatResponse

# just a rough list for now of which errors mean "try someone else"
# vs which ones mean "this is genuinely broken, dont bother retrying"
# gonna refine this as i learn more about what each sdk actually throws

class AllProvidersFailedError(Exception):
    # raised when literally every provider in the list failed
    pass


# maps a quality level to (which provider to try first, which model to use)
# ordered by preference - first one in each list is tried first

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
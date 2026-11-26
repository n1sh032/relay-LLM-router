from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.application import close_router, configure_router
from app.body_limit import ChatBodyLimit
from app.providers.base import ChatRequest, ChatResponse
from app.routing.router import AllProvidersFailedError

load_dotenv()
router = configure_router()

app.add_middleware(ChatBodyLimit)

# openai first, gemini as backup if it fails
def configure_router():
    providers = {}
    for name, key, factory in (
        ("openai", "OPENAI_API_KEY", OpenAIProvider),
        ("gemini", "GEMINI_API_KEY", GeminiProvider),
    ):
        reason = "missing_api_key"
        if os.getenv(key, "").strip():
            try:
                providers[name] = factory()
                continue
            except Exception as exc:
                reason = type(exc).__name__
        logging.getLogger(__name__).warning(json.dumps({
            "event": "provider_unavailable", "provider": name,
            "setting": key, "reason": reason,
        }))
    return Router(providers)


router = configure_router()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not router.providers:
        raise HTTPException(503, detail={"code": "no_providers_configured"})
    try:
        return await router.chat(request)
    except AllProvidersFailedError:
        raise HTTPException(502, detail={"code": "providers_failed"}) from None

import json
import logging
import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from app.providers.base import ChatRequest, ChatResponse
from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.routing.router import AllProvidersFailedError, Router

app = FastAPI()

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

@app.post("/chat")
async def chat(request: ChatRequest):
    return await router.chat(request)
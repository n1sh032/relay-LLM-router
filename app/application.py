"""Provider composition and lifecycle for the API."""
import json
import logging
import os

from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider
from app.routing.router import Router

logger = logging.getLogger(__name__)


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
        logger.warning(json.dumps({
            "event": "provider_unavailable", "provider": name, "setting": key, "reason": reason,
        }))
    return Router(providers)


async def close_router(router):
    for name, provider in router.providers.items():
        try:
            await provider.close()
        except Exception:
            logger.exception("Provider cleanup failed", extra={"provider": name})

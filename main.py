from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.application import close_router, configure_router
from app.body_limit import ChatBodyLimit
from app.providers.base import ChatRequest, ChatResponse
from app.routing.router import AllProvidersFailedError

load_dotenv()
router = configure_router()


@asynccontextmanager
async def lifespan(app):
    try:
        yield
    finally:
        await close_router(router)


app = FastAPI(title="Relay LLM Router", version="0.1.0", lifespan=lifespan)
app.add_middleware(ChatBodyLimit)


@app.get("/health")
async def health():
    return {"status": "ready" if router.providers else "unconfigured",
            "providers": sorted(router.providers)}

router = configure_router()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not router.providers:
        raise HTTPException(503, detail={"code": "no_providers_configured"})
    try:
        return await router.chat(request)
    except AllProvidersFailedError:
        raise HTTPException(502, detail={"code": "providers_failed"}) from None

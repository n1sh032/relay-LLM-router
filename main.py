from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.providers.base import ChatRequest
from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.routing.router import Router

app = FastAPI()

# openai first, gemini as backup if it fails
router = Router({
    "openai": OpenAIProvider(),
    "gemini": GeminiProvider(),
})

@app.post("/chat")
async def chat(request: ChatRequest):
    return await router.chat(request)
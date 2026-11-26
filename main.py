from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.providers.base import ChatRequest
from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.routing.router import Router

app = FastAPI()

# just hardcoding these for now, will build real routing later
openai_provider = OpenAIProvider()
gemini_provider = GeminiProvider()


@app.post("/chat")
async def chat(request: ChatRequest):
    # super basic for now - if model name has "gemini" in it use gemini,
    # otherwise just default to openai. will replace this with real
    # routing logic later
    if "gemini" in request.model.lower():
        return await gemini_provider.chat(request)
    else:
        return await openai_provider.chat(request)
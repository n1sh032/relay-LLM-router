from dotenv import load_dotenv
load_dotenv()  # this reads .env and loads OPENAI_API_KEY etc into the environment

from fastapi import FastAPI
from app.providers.base import ChatRequest
from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider

app = FastAPI()

# just hardcoding these for now, will build real routing later
openai_provider = OpenAIProvider()
gemini_provider = GeminiProvider()



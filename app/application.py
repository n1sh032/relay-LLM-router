"""Provider composition and lifecycle for the API."""
import json
import logging
import os

from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider
from app.routing.router import Router


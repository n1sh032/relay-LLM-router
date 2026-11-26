import os
import google.generativeai as genai
from app.providers.base import Provider, ChatRequest, ChatResponse

# gemini needs to be configured globally with the key first
# before you can even create a model object, kinda annoying

from abc import ABC, abstractmethod
from pydantic import BaseModel

# these are the "shapes" my gateway uses internally
# doesnt matter if its openai or gemini underneath, everything gets
# converted into these before it leaves the provider files

class ChatMessage(BaseModel):
    role: str       # "user", "assistant" or "system"
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    quality: str = "fast"  # "fast" or "smart" for now
    model: str | None = None  # router fills this in, dont need to set it yourself
    max_tokens: int | None = None
    temperature: float | None = None

class ChatResponse(BaseModel):
    content: str
    provider: str  # so i can tell which one actually answered
    model: str
    input_tokens: int
    output_tokens: int

class Provider(ABC):
    # every provider (openai, gemini etc) has to implement this
    # keeps everything consistent so the router doesnt care who its talking to

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        pass

    # TODO: add health_check() later maybe, so i can ping providers
    # before routing to them instead of just finding out when it fails
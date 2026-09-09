from abc import ABC, abstractmethod
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: str
    max_tokens: int | None = None
    temperature: float | None = None


class ChatResponse(BaseModel):
    content: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int


class Provider(ABC):
    """
    Base contract every provider (OpenAI, Gemini, etc.) must follow.
    The rest of the gateway only ever talks to this interface,
    so it never needs to know which real provider is underneath.
    """

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Send a chat request to the provider, return a normalized response."""
        ...
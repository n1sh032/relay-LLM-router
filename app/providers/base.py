from abc import ABC, abstractmethod
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

# these are the "shapes" my gateway uses internally
# doesnt matter if its openai or gemini underneath, everything gets
# converted into these before it leaves the provider files

class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1, max_length=16000)

class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    messages: list[ChatMessage] = Field(min_length=1, max_length=64)
    quality: Literal["fast", "smart"] = "fast"
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
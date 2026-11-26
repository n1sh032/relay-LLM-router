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
    max_tokens: int | None = Field(None, ge=1, le=8192, strict=True)
    temperature: float | None = Field(None, ge=0, le=2, strict=True)

    @model_validator(mode="after")
    def validate_messages(self):
        if any(not m.content.strip() for m in self.messages):
            raise ValueError("messages cannot be blank")
        if sum(len(m.content) for m in self.messages) > 64000:
            raise ValueError("combined message content cannot exceed 64000 characters")
        if not any(m.role == "user" for m in self.messages):
            raise ValueError("at least one user message is required")
        if any(m.role == "system" for m in self.messages[1:]):
            raise ValueError("a system message is only allowed at the start")
        if self.model is not None:
            raise ValueError("choose a quality tier instead of specifying a model")
        return self

class ChatResponse(BaseModel):
    content: str
    provider: str  # so i can tell which one actually answered
    model: str
    input_tokens: int | None
    output_tokens: int | None


class Provider(ABC):
    # every provider (openai, gemini etc) has to implement this
    # keeps everything consistent so the router doesnt care who its talking to

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        pass

    # TODO: add health_check() later maybe, so i can ping providers
    # before routing to them instead of just finding out when it fails
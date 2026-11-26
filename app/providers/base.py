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

from abc import ABC, abstractmethod
from pydantic import BaseModel

# these are the "shapes" my gateway uses internally
# doesn't matter if its openai or gemini underneath, everything gets
# converted into these before it leaves the provider files

class ChatMessage(BaseModel):
    role: str       # "user", "assistant" or "system"
    content: str


class ChatRequest(BaseModel):
    # this is what comes IN to my api
    messages: list[ChatMessage]
    model: str
    max_tokens: int | None = None
    temperature: float | None = None


class ChatResponse(BaseModel):
    # this is what goes OUT, no matter which provider handled it
    content: str
    provider: str      # so i can see in logs which one actually answered
    model: str
    input_tokens: int
    output_tokens: int


# base class / interface that every provider has to follow
# using ABC here so python actually forces subclasses to implement chat()
# instead of me forgetting and it just breaking randomly later

class Provider(ABC):

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        # every provider needs to take my ChatRequest format
        # and return my ChatResponse format, doesn't matter how
        # they do it internally
        pass

    # TODO: maybe add a health_check() method later so i can ping
    # providers and see which ones are up before routing to them
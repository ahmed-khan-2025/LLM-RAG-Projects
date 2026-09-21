from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
    )


class SourceResponse(BaseModel):
    source: str
    start: float
    end: float
    text: str
    score: float | None = None
    retrieval_sources: list[str]


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]


class IndexResponse(BaseModel):
    source: str
    chunks_created: int
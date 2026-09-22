from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    question: str = Field(
        min_length=1,
        max_length=2000,
    )


class SourceResponse(BaseModel):

    source: str
    modality: str
    start: float
    end: float
    text: str
    score: float | None = None
    retrieval_sources: list[str]
    frame_path: str | None = None


class ChatResponse(BaseModel):

    question: str
    answer: str
    sources: list[SourceResponse]


class VideoIndexResponse(BaseModel):

    source: str
    language: str
    duration: float
    audio_chunks: int
    visual_chunks: int
    total_chunks: int
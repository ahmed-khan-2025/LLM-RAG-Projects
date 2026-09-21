from dataclasses import dataclass, field
from typing import Any


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str
    words: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class DocumentChunk:
    id: str
    text: str
    source: str
    start: float
    end: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrievedDocument:
    chunk: DocumentChunk
    score: float
    source_type: str
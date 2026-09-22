from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentChunk:
    id: str
    text: str
    source: str
    modality: str
    start: float
    end: float
    metadata: dict[str, Any] = field(default_factory=dict)
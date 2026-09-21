import re
import uuid
from typing import Any

from app.rag.models import DocumentChunk


class TranscriptChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def chunk(
        self,
        transcript: dict[str, Any],
        source: str,
    ) -> list[DocumentChunk]:

        segments = transcript["segments"]

        chunks: list[DocumentChunk] = []

        current_segments = []
        current_length = 0

        for segment in segments:
            text = self._clean_text(segment["text"])

            if not text:
                continue

            segment_length = len(text)

            if (
                current_segments
                and current_length + segment_length
                > self.chunk_size
            ):
                chunks.append(
                    self._create_chunk(
                        current_segments,
                        source,
                    )
                )

                overlap_segments = self._get_overlap_segments(
                    current_segments
                )

                current_segments = overlap_segments
                current_length = sum(
                    len(item["text"])
                    for item in current_segments
                )

            current_segments.append(
                {
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": text,
                }
            )

            current_length += segment_length

        if current_segments:
            chunks.append(
                self._create_chunk(
                    current_segments,
                    source,
                )
            )

        return chunks

    def _get_overlap_segments(
        self,
        segments: list[dict],
    ) -> list[dict]:

        result = []
        length = 0

        for segment in reversed(segments):
            result.insert(0, segment)
            length += len(segment["text"])

            if length >= self.chunk_overlap:
                break

        return result

    def _create_chunk(
        self,
        segments: list[dict],
        source: str,
    ) -> DocumentChunk:

        text = " ".join(
            segment["text"]
            for segment in segments
        )

        return DocumentChunk(
            id=str(uuid.uuid4()),
            text=text,
            source=source,
            start=segments[0]["start"],
            end=segments[-1]["end"],
            metadata={
                "source": source,
                "start": segments[0]["start"],
                "end": segments[-1]["end"],
            },
        )
import re
import uuid

from app.rag.models import DocumentChunk


class MultimodalChunker:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _clean(
        self,
        text: str,
    ) -> str:

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    def chunk_audio(
        self,
        transcript: dict,
        source: str,
    ) -> list[DocumentChunk]:

        segments = transcript[
            "segments"
        ]

        chunks = []

        current = []
        length = 0

        for segment in segments:

            text = self._clean(
                segment["text"]
            )

            if not text:
                continue

            if (
                current
                and length + len(text)
                > self.chunk_size
            ):

                chunks.append(
                    self._create_audio_chunk(
                        current,
                        source,
                    )
                )

                current = current[
                    -2:
                ]

                length = sum(
                    len(x["text"])
                    for x in current
                )

            current.append(
                {
                    "start": segment[
                        "start"
                    ],
                    "end": segment[
                        "end"
                    ],
                    "text": text,
                }
            )

            length += len(text)

        if current:

            chunks.append(
                self._create_audio_chunk(
                    current,
                    source,
                )
            )

        return chunks

    def _create_audio_chunk(
        self,
        segments: list[dict],
        source: str,
    ) -> DocumentChunk:

        text = " ".join(
            item["text"]
            for item in segments
        )

        start = segments[0]["start"]
        end = segments[-1]["end"]

        return DocumentChunk(
            id=str(uuid.uuid4()),
            text=text,
            source=source,
            modality="audio",
            start=start,
            end=end,
            metadata={
                "source": source,
                "modality": "audio",
                "start": start,
                "end": end,
            },
        )

    def create_visual_chunk(
        self,
        description: str,
        source: str,
        timestamp: float,
        frame_path: str,
    ) -> DocumentChunk:

        text = self._clean(
            description
        )

        return DocumentChunk(
            id=str(uuid.uuid4()),
            text=text,
            source=source,
            modality="visual",
            start=timestamp,
            end=timestamp,
            metadata={
                "source": source,
                "modality": "visual",
                "start": timestamp,
                "end": timestamp,
                "frame_path": frame_path,
            },
        )
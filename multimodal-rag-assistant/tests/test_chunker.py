from app.rag.chunker import (
    MultimodalChunker,
)


def test_audio_chunking():

    transcript = {
        "segments": [
            {
                "start": 0,
                "end": 5,
                "text": (
                    "Welcome to the meeting."
                ),
            },
            {
                "start": 5,
                "end": 10,
                "text": (
                    "Today we discuss "
                    "the project."
                ),
            },
            {
                "start": 10,
                "end": 15,
                "text": (
                    "The project budget "
                    "is important."
                ),
            },
        ]
    }

    chunker = MultimodalChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunker.chunk_audio(
        transcript,
        "meeting.mp4",
    )

    assert len(chunks) > 0

    assert (
        chunks[0].source
        == "meeting.mp4"
    )

    assert (
        chunks[0].modality
        == "audio"
    )


def test_visual_chunk():

    chunker = MultimodalChunker()

    chunk = (
        chunker.create_visual_chunk(
            description=(
                "A laptop screen "
                "shows a chart."
            ),
            source="meeting.mp4",
            timestamp=120,
            frame_path=(
                "data/frames/frame.jpg"
            ),
        )
    )

    assert chunk.modality == "visual"

    assert chunk.start == 120

    assert (
        "laptop"
        in chunk.text.lower()
    )
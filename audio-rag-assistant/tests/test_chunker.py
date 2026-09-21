from app.rag.chunker import TranscriptChunker


def test_chunker_creates_chunks():

    transcript = {
        "segments": [
            {
                "start": 0,
                "end": 5,
                "text": "This is the first sentence.",
            },
            {
                "start": 5,
                "end": 10,
                "text": "This is the second sentence.",
            },
            {
                "start": 10,
                "end": 15,
                "text": "This is the third sentence.",
            },
        ]
    }

    chunker = TranscriptChunker(
        chunk_size=50,
        chunk_overlap=10,
    )

    chunks = chunker.chunk(
        transcript,
        "test.mp3",
    )

    assert len(chunks) > 0

    assert chunks[0].source == "test.mp3"

    assert chunks[0].start == 0
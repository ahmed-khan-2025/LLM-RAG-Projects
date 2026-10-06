from app.ingestion.chunker import chunk_text

def test_chunk_text():
    text = "This is a test. " * 300
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)

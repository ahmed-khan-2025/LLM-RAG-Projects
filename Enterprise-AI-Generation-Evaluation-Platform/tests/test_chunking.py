from app.services.ingestion import chunk_text

def test_chunking():
    chunks=chunk_text('hello world '*500,chunk_size=100,overlap=20)
    assert len(chunks)>1
    assert all(chunks)

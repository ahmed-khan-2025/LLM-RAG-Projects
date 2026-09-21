from pathlib import Path

import chromadb

from app.rag.embeddings import EmbeddingModel
from app.rag.models import DocumentChunk


class VectorStore:
    def __init__(
        self,
        path: str,
        collection_name: str,
        embedding_model: EmbeddingModel,
    ):
        Path(path).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=path
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "hnsw:space": "cosine"
            },
        )

        self.embedding_model = embedding_model

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
    ):

        if not chunks:
            return

        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = self.embedding_model.encode(texts)

        ids = [
            chunk.id
            for chunk in chunks
        ]

        metadatas = [
            {
                "source": chunk.source,
                "start": chunk.start,
                "end": chunk.end,
            }
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query: str,
        top_k: int = 8,
    ) -> list[dict]:

        query_embedding = (
            self.embedding_model.encode_query(query)
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        output = []

        for i in range(len(documents)):
            output.append(
                {
                    "id": ids[i],
                    "text": documents[i],
                    "metadata": metadatas[i],
                    "distance": distances[i],
                }
            )

        return output
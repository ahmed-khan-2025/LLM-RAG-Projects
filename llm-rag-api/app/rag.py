from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from .documents import load_document, split_text


class RAGSystem:

    def __init__(self, document_path: str):
        self.document_path = document_path

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Loading document...")

        text = load_document(document_path)

        self.chunks = split_text(
            text,
            chunk_size=100
        )

        print(f"Created {len(self.chunks)} document chunks.")

        print("Creating embeddings...")

        self.embeddings = self.model.encode(
            self.chunks,
            convert_to_numpy=True
        )

        self.embeddings = self._normalize(
            self.embeddings
        )

        print("RAG system ready.")

    @staticmethod
    def _normalize(vectors):
        norms = np.linalg.norm(
            vectors,
            axis=1,
            keepdims=True
        )

        return vectors / (norms + 1e-10)

    def search(
        self,
        question: str,
        top_k: int = 3
    ):
        question_embedding = self.model.encode(
            [question],
            convert_to_numpy=True
        )

        question_embedding = self._normalize(
            question_embedding
        )

        scores = np.dot(
            self.embeddings,
            question_embedding[0]
        )

        indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for index in indices:
            results.append(
                {
                    "text": self.chunks[index],
                    "score": float(scores[index])
                }
            )

        return results
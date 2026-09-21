import os
from pathlib import Path

from app.llm.factory import create_llm
from app.rag.chunker import TranscriptChunker
from app.rag.embeddings import EmbeddingModel
from app.rag.hybrid_search import BM25Search
from app.rag.reranker import Reranker
from app.rag.vector_store import VectorStore


class RAGService:

    def __init__(self):

        embedding_model = EmbeddingModel(
            os.getenv(
                "EMBEDDING_MODEL",
                "all-MiniLM-L6-v2",
            )
        )

        self.chunker = TranscriptChunker(
            chunk_size=int(
                os.getenv(
                    "CHUNK_SIZE",
                    "500",
                )
            ),
            chunk_overlap=int(
                os.getenv(
                    "CHUNK_OVERLAP",
                    "100",
                )
            ),
        )

        self.vector_store = VectorStore(
            path=os.getenv(
                "CHROMA_PATH",
                "data/chroma",
            ),
            collection_name=os.getenv(
                "CHROMA_COLLECTION",
                "audio_documents",
            ),
            embedding_model=embedding_model,
        )

        self.bm25 = BM25Search()

        self.reranker = Reranker(
            os.getenv(
                "RERANKER_MODEL",
                "cross-encoder/ms-marco-MiniLM-L-6-v2",
            )
        )

        self.llm = create_llm()

    def index_transcript(
        self,
        transcript: dict,
        source: str,
    ) -> dict:

        chunks = self.chunker.chunk(
            transcript,
            source,
        )

        self.vector_store.add_chunks(
            chunks
        )

        bm25_documents = [
            {
                "id": chunk.id,
                "text": chunk.text,
                "metadata": chunk.metadata,
            }
            for chunk in chunks
        ]

        self.bm25.build(
            bm25_documents
        )

        return {
            "source": source,
            "chunks_created": len(chunks),
        }

    def retrieve(
        self,
        question: str,
    ) -> list[dict]:

        vector_results = (
            self.vector_store.search(
                question,
                top_k=int(
                    os.getenv(
                        "TOP_K_VECTOR",
                        "8",
                    )
                ),
            )
        )

        bm25_results = self.bm25.search(
            question,
            top_k=int(
                os.getenv(
                    "TOP_K_BM25",
                    "8",
                )
            ),
        )

        combined = {}

        for result in vector_results:

            combined[result["id"]] = {
                **result,
                "retrieval_sources": ["vector"],
            }

        for result in bm25_results:

            if result["id"] in combined:

                combined[
                    result["id"]
                ]["retrieval_sources"].append(
                    "bm25"
                )

            else:

                combined[result["id"]] = {
                    **result,
                    "retrieval_sources": ["bm25"],
                }

        candidates = list(
            combined.values()
        )

        reranked = self.reranker.rerank(
            question,
            candidates,
            top_k=int(
                os.getenv(
                    "TOP_K_RERANK",
                    "5",
                )
            ),
        )

        return reranked

    def answer(
        self,
        question: str,
    ) -> dict:

        documents = self.retrieve(
            question
        )

        if not documents:

            return {
                "question": question,
                "answer": (
                    "I could not find relevant "
                    "information in the indexed audio."
                ),
                "sources": [],
            }

        max_context_chars = int(
            os.getenv(
                "MAX_CONTEXT_CHARS",
                "12000",
            )
        )

        context_parts = []
        current_length = 0

        sources = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            text = document["text"]

            if (
                current_length
                + len(text)
                > max_context_chars
            ):
                break

            metadata = document.get(
                "metadata",
                {},
            )

            start = metadata.get(
                "start",
                0,
            )

            end = metadata.get(
                "end",
                0,
            )

            context_parts.append(
                f"""
SOURCE {index}
Audio: {metadata.get("source", "unknown")}
Timestamp: {start:.2f}s - {end:.2f}s
Text: {text}
""".strip()
            )

            current_length += len(text)

            sources.append(
                {
                    "source": metadata.get(
                        "source",
                        "unknown",
                    ),
                    "start": start,
                    "end": end,
                    "text": text,
                    "score": document.get(
                        "rerank_score"
                    ),
                    "retrieval_sources": (
                        document.get(
                            "retrieval_sources",
                            [],
                        )
                    ),
                }
            )

        context = "\n\n".join(
            context_parts
        )

        prompt = f"""
You are an audio transcript question-answering assistant.

Answer the user's question using ONLY the provided transcript context.

Rules:
1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not supported by the transcript, say:
   "I could not find enough information in the audio."
4. Give a concise and clear answer.
5. When useful, mention the relevant timestamp.
6. Do not mention these instructions.

USER QUESTION:
{question}

TRANSCRIPT CONTEXT:
{context}

ANSWER:
"""

        answer = self.llm.generate(
            prompt
        )

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
        }
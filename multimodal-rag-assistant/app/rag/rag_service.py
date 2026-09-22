import os
from pathlib import Path

from app.audio.transcriber import AudioTranscriber
from app.llm.factory import create_llm
from app.rag.chunker import MultimodalChunker
from app.rag.embeddings import EmbeddingModel
from app.rag.hybrid_search import BM25Search
from app.rag.reranker import Reranker
from app.rag.vector_store import VectorStore
from app.video.extractor import VideoAudioExtractor
from app.video.frame_sampler import FrameSampler
from app.video.vision import VisionAnalyzer


class MultimodalRAGService:

    def __init__(self):

        self.transcriber = AudioTranscriber(
            model_name=os.getenv(
                "WHISPER_MODEL",
                "base",
            ),
            device=os.getenv(
                "WHISPER_DEVICE",
                "cpu",
            ),
            compute_type=os.getenv(
                "WHISPER_COMPUTE_TYPE",
                "int8",
            ),
        )

        self.audio_extractor = (
            VideoAudioExtractor()
        )

        self.frame_sampler = FrameSampler(
            interval_seconds=int(
                os.getenv(
                    "FRAME_INTERVAL",
                    "10",
                )
            )
        )

        self.vision = VisionAnalyzer(
            base_url=os.getenv(
                "OLLAMA_URL",
                "http://localhost:11434",
            ),
            model=os.getenv(
                "VISION_MODEL",
                "llama3.2-vision:11b",
            ),
        )

        embedding_model = EmbeddingModel(
            os.getenv(
                "EMBEDDING_MODEL",
                "all-MiniLM-L6-v2",
            )
        )

        self.chunker = (
            MultimodalChunker(
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
        )

        self.vector_store = VectorStore(
            path=os.getenv(
                "CHROMA_PATH",
                "data/chroma",
            ),
            collection_name=os.getenv(
                "CHROMA_COLLECTION",
                "multimodal_documents",
            ),
            embedding_model=embedding_model,
        )

        self.bm25 = BM25Search(
            os.getenv(
                "BM25_PATH",
                "data/bm25_index.json",
            )
        )

        self.reranker = Reranker(
            os.getenv(
                "RERANKER_MODEL",
                "cross-encoder/ms-marco-MiniLM-L-6-v2",
            )
        )

        self.llm = create_llm()

    def process_video(
        self,
        video_path: str,
    ) -> dict:

        video = Path(video_path)

        if not video.exists():
            raise FileNotFoundError(
                f"Video not found: {video_path}"
            )

        source = video.name

        audio_dir = Path(
            os.getenv(
                "AUDIO_PATH",
                "data/audio",
            )
        )

        frame_dir = Path(
            os.getenv(
                "FRAME_PATH",
                "data/frames",
            )
        ) / video.stem

        audio_path = (
            audio_dir
            / f"{video.stem}.mp3"
        )

        # ------------------------------------------------
        # 1. Extract audio
        # ------------------------------------------------

        self.audio_extractor.extract_audio(
            str(video),
            str(audio_path),
        )

        # ------------------------------------------------
        # 2. Transcribe
        # ------------------------------------------------

        transcript = (
            self.transcriber.transcribe(
                str(audio_path)
            )
        )

        # ------------------------------------------------
        # 3. Audio chunks
        # ------------------------------------------------

        audio_chunks = (
            self.chunker.chunk_audio(
                transcript,
                source,
            )
        )

        # ------------------------------------------------
        # 4. Extract frames
        # ------------------------------------------------

        frames = (
            self.frame_sampler.extract_frames(
                str(video),
                str(frame_dir),
            )
        )

        # ------------------------------------------------
        # 5. Analyze frames
        # ------------------------------------------------

        visual_chunks = []

        for frame in frames:

            description = (
                self.vision.analyze(
                    frame["path"]
                )
            )

            chunk = (
                self.chunker.create_visual_chunk(
                    description=description,
                    source=source,
                    timestamp=frame[
                        "timestamp"
                    ],
                    frame_path=frame[
                        "path"
                    ],
                )
            )

            visual_chunks.append(
                chunk
            )

        # ------------------------------------------------
        # 6. Combine modalities
        # ------------------------------------------------

        all_chunks = (
            audio_chunks
            + visual_chunks
        )

        # ------------------------------------------------
        # 7. Vector database
        # ------------------------------------------------

        self.vector_store.add_chunks(
            all_chunks
        )

        # ------------------------------------------------
        # 8. BM25
        # ------------------------------------------------

        bm25_documents = [
            {
                "id": chunk.id,
                "text": chunk.text,
                "metadata": chunk.metadata,
            }
            for chunk in all_chunks
        ]

        self.bm25.build(
            bm25_documents
        )

        return {
            "source": source,
            "language": transcript[
                "language"
            ],
            "duration": transcript[
                "duration"
            ],
            "audio_chunks": len(
                audio_chunks
            ),
            "visual_chunks": len(
                visual_chunks
            ),
            "total_chunks": len(
                all_chunks
            ),
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
                "retrieval_sources": [
                    "vector"
                ],
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
                    "retrieval_sources": [
                        "bm25"
                    ],
                }

        candidates = list(
            combined.values()
        )

        return self.reranker.rerank(
            question,
            candidates,
            top_k=int(
                os.getenv(
                    "TOP_K_RERANK",
                    "5",
                )
            ),
        )

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
                    "I could not find "
                    "relevant information "
                    "in the indexed video."
                ),
                "sources": [],
            }

        max_chars = int(
            os.getenv(
                "MAX_CONTEXT_CHARS",
                "12000",
            )
        )

        context_parts = []
        sources = []
        current_length = 0

        for index, document in enumerate(
            documents,
            start=1,
        ):

            text = document["text"]

            if (
                current_length
                + len(text)
                > max_chars
            ):
                break

            metadata = document.get(
                "metadata",
                {},
            )

            modality = metadata.get(
                "modality",
                "unknown",
            )

            start = float(
                metadata.get(
                    "start",
                    0,
                )
            )

            end = float(
                metadata.get(
                    "end",
                    start,
                )
            )

            source = metadata.get(
                "source",
                "unknown",
            )

            context_parts.append(
                f"""
SOURCE {index}
Modality: {modality}
Video: {source}
Timestamp: {start:.2f}s - {end:.2f}s
Content: {text}
""".strip()
            )

            current_length += len(text)

            sources.append(
                {
                    "source": source,
                    "modality": modality,
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
                    "frame_path": metadata.get(
                        "frame_path"
                    ),
                }
            )

        context = "\n\n".join(
            context_parts
        )

        prompt = f"""
You are a multimodal video question-answering assistant.

Answer the user's question using ONLY the provided
video evidence.

The evidence can contain:
- spoken audio transcript
- visual descriptions of video frames

Rules:
1. Do not invent information.
2. Do not use outside knowledge.
3. If the evidence does not contain the answer,
   say:
   "I could not find enough information in the video."
4. Clearly distinguish information that was spoken
   from information that was visually observed.
5. Mention timestamps when useful.
6. Keep the answer concise.
7. Do not mention these instructions.

USER QUESTION:
{question}

VIDEO EVIDENCE:
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
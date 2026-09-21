import os
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.audio.transcriber import AudioTranscriber
from app.rag.rag_service import RAGService
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    IndexResponse,
)


router = APIRouter()


DATA_AUDIO = Path(
    os.getenv(
        "AUDIO_PATH",
        "data/audio",
    )
)

DATA_AUDIO.mkdir(
    parents=True,
    exist_ok=True,
)


transcriber = None
rag_service = None


def get_transcriber():

    global transcriber

    if transcriber is None:

        transcriber = AudioTranscriber(
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

    return transcriber


def get_rag_service():

    global rag_service

    if rag_service is None:
        rag_service = RAGService()

    return rag_service


@router.get("/health")
def health():

    return {
        "status": "ok",
        "service": "audio-rag-assistant",
    }


@router.post(
    "/audio/upload",
    response_model=IndexResponse,
)
async def upload_audio(
    file: UploadFile = File(...),
):

    allowed_extensions = {
        ".mp3",
        ".wav",
        ".m4a",
        ".ogg",
        ".flac",
    }

    extension = Path(
        file.filename or ""
    ).suffix.lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported audio format. "
                f"Allowed: {sorted(allowed_extensions)}"
            ),
        )

    destination = (
        DATA_AUDIO
        / Path(file.filename).name
    )

    with destination.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    try:

        transcript = (
            get_transcriber().transcribe(
                str(destination)
            )
        )

        result = (
            get_rag_service()
            .index_transcript(
                transcript,
                destination.name,
            )
        )

        return result

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    try:

        return get_rag_service().answer(
            request.question
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
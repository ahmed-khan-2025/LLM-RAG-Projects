import os
import shutil
from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.rag.rag_service import (
    MultimodalRAGService,
)
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    VideoIndexResponse,
)


router = APIRouter()


VIDEO_PATH = Path(
    os.getenv(
        "VIDEO_PATH",
        "data/videos",
    )
)

VIDEO_PATH.mkdir(
    parents=True,
    exist_ok=True,
)


rag_service = None


def get_rag_service():

    global rag_service

    if rag_service is None:
        rag_service = (
            MultimodalRAGService()
        )

    return rag_service


@router.get("/health")
def health():

    return {
        "status": "ok",
        "service": (
            "multimodal-rag-assistant"
        ),
    }


@router.post(
    "/video/upload",
    response_model=VideoIndexResponse,
)
async def upload_video(
    file: UploadFile = File(...),
):

    allowed_extensions = {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".webm",
    }

    extension = Path(
        file.filename or ""
    ).suffix.lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported video format. "
                f"Allowed: "
                f"{sorted(allowed_extensions)}"
            ),
        )

    filename = Path(
        file.filename
    ).name

    destination = (
        VIDEO_PATH / filename
    )

    with destination.open("wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    try:

        result = (
            get_rag_service()
            .process_video(
                str(destination)
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

        return (
            get_rag_service()
            .answer(
                request.question
            )
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
from pathlib import Path
from typing import Any

from faster_whisper import WhisperModel


class AudioTranscriber:

    def __init__(
        self,
        model_name: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self.model = WhisperModel(
            model_name,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(
        self,
        audio_path: str,
    ) -> dict[str, Any]:

        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        segments, info = self.model.transcribe(
            str(path),
            beam_size=5,
            vad_filter=True,
            word_timestamps=True,
        )

        result_segments = []

        for segment in segments:

            result_segments.append(
                {
                    "start": round(
                        segment.start,
                        2,
                    ),
                    "end": round(
                        segment.end,
                        2,
                    ),
                    "text": segment.text.strip(),
                }
            )

        full_text = " ".join(
            segment["text"]
            for segment in result_segments
        )

        return {
            "language": info.language,
            "language_probability": (
                info.language_probability
            ),
            "duration": info.duration,
            "text": full_text.strip(),
            "segments": result_segments,
        }
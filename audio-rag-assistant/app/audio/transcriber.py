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

    def transcribe(self, audio_path: str) -> dict[str, Any]:
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
            words = []

            if segment.words:
                for word in segment.words:
                    words.append(
                        {
                            "start": word.start,
                            "end": word.end,
                            "word": word.word.strip(),
                        }
                    )

            result_segments.append(
                {
                    "start": round(segment.start, 2),
                    "end": round(segment.end, 2),
                    "text": segment.text.strip(),
                    "words": words,
                }
            )

        full_text = " ".join(
            item["text"]
            for item in result_segments
            if item["text"]
        )

        return {
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "text": full_text,
            "segments": result_segments,
        }
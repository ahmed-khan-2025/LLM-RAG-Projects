import subprocess
from pathlib import Path


class VideoAudioExtractor:

    def extract_audio(
        self,
        video_path: str,
        output_path: str,
    ) -> str:

        video = Path(video_path)
        output = Path(output_path)

        if not video.exists():
            raise FileNotFoundError(
                f"Video not found: {video_path}"
            )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-vn",
            "-acodec",
            "mp3",
            str(output),
        ]

        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return str(output)
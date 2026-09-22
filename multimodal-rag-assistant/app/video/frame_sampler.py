from pathlib import Path

import cv2


class FrameSampler:

    def __init__(
        self,
        interval_seconds: int = 10,
    ):
        self.interval_seconds = interval_seconds

    def extract_frames(
        self,
        video_path: str,
        output_dir: str,
    ) -> list[dict]:

        video = cv2.VideoCapture(
            video_path
        )

        if not video.isOpened():
            raise RuntimeError(
                f"Could not open video: {video_path}"
            )

        output = Path(output_dir)
        output.mkdir(
            parents=True,
            exist_ok=True,
        )

        fps = video.get(
            cv2.CAP_PROP_FPS
        )

        frame_count = int(
            video.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        duration = (
            frame_count / fps
            if fps > 0
            else 0
        )

        frames = []

        timestamp = 0.0

        while timestamp < duration:

            video.set(
                cv2.CAP_PROP_POS_MSEC,
                timestamp * 1000,
            )

            success, frame = video.read()

            if not success:
                break

            filename = (
                f"frame_{int(timestamp):06d}.jpg"
            )

            frame_path = output / filename

            cv2.imwrite(
                str(frame_path),
                frame,
            )

            frames.append(
                {
                    "path": str(frame_path),
                    "timestamp": round(
                        timestamp,
                        2,
                    ),
                }
            )

            timestamp += (
                self.interval_seconds
            )

        video.release()

        return frames
from __future__ import annotations

from pathlib import Path
import time
from typing import Any, Optional, Tuple

import cv2


class Camera:
    """Verantwoordelijk voor het ophalen van frames en het maken van snapshots."""

    def __init__(
        self,
        *,
        stream_url: str = "http://172.20.10.10:81/stream",
        cascade_path: str = cv2.data.haarcascades + "haarcascade_frontalface_default.xml",
        snapshot_path: Path | str = Path("snapshots/candidate.jpg"),
        face_hold_seconds: float = 2.0,
        padding_ratio: float = 0.5,
        resolution: Tuple[int, int] = (640, 480),
    ) -> None:
        self.camera_index = stream_url
        self.resolution = resolution
        self.face_hold_seconds = face_hold_seconds
        self.padding_ratio = padding_ratio
        self.snapshot_path = Path(snapshot_path)
        self.snapshot_path.parent.mkdir(parents=True, exist_ok=True)

        self._detected_since: Optional[float] = None
        self._snapshot_available = False
        self._last_snapshot_time: Optional[float] = None

        self._face_detector = cv2.CascadeClassifier(cascade_path)
        if self._face_detector.empty():
            raise RuntimeError(f"Kon Haar-cascade niet laden: {cascade_path}")

        self._cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
        if not self._cap.isOpened():
            raise RuntimeError(f"Kan stream niet openen: {stream_url}")

    def snapshot(self) -> Optional[Any]:
        ok, frame = self._cap.read()
        if not ok:
            return None

        frame = cv2.resize(frame, self.resolution, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=6,
            minSize=(80, 80),
        )

        if len(faces):
            x, y, w, h = max(faces, key=lambda box: box[2] * box[3])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)

            now = time.time()
            if self._detected_since is None:
                self._detected_since = now
            elif now - self._detected_since >= self.face_hold_seconds:
                self._save_snapshot(frame, (x, y, w, h))
                self._detected_since = None
        else:
            self._detected_since = None

        return frame

    def _save_snapshot(self, frame, face_box) -> None:
        x, y, w, h = face_box
        pad = int(max(w, h) * self.padding_ratio)
        x1 = max(x - pad, 0)
        y1 = max(y - pad, 0)
        x2 = min(x + w + pad, frame.shape[1])
        y2 = min(y + h + pad, frame.shape[0])

        face_roi = frame[y1:y2, x1:x2]
        cv2.imwrite(str(self.snapshot_path), face_roi)
        self._snapshot_available = True
        self._last_snapshot_time = time.time()

    def poll_snapshot(self) -> Optional[Path]:
        if self._snapshot_available and self.snapshot_path.exists():
            self._snapshot_available = False
            return self.snapshot_path
        return None

    def snapshot_age(self) -> Optional[float]:
        if self._last_snapshot_time is None:
            return None
        return time.time() - self._last_snapshot_time

    def release(self) -> None:
        if self._cap.isOpened():
            self._cap.release()

    def __del__(self) -> None:  # pragma: no cover - best effort cleanup
        try:
            self.release()
        except Exception:
            pass


if __name__ == "__main__":
    cam = Camera()
    try:
        while True:
            frame = cam.snapshot()
            if frame is None:
                continue
            cv2.imshow("Camera Test", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()
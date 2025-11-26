from pathlib import Path
import time

import cv2
import serial

ESP32_STREAM_URL = "http://172.20.10.8:81/stream"  # pas aan naar de ESP32 IP
SERIAL_PORT = "COM3"  # pas aan naar de juiste COM-poort
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
SNAPSHOT_PATH = Path("snapshots/candidate.jpg")
FACE_HOLD_SECONDS = 2.0

face_detector = cv2.CascadeClassifier(CASCADE_PATH)
if face_detector.empty():
    raise RuntimeError(f"Kon Haar-cascade niet laden: {CASCADE_PATH}")

SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(ESP32_STREAM_URL)
if not cap.isOpened():
    raise RuntimeError(f"Kan stream niet openen: {ESP32_STREAM_URL}")

ser = serial.Serial(SERIAL_PORT, 115200, timeout=1)
time.sleep(2)  # wacht tot Arduino klaar is

detected_since: float | None = None

try:
    while True:
        ok, frame = cap.read()
        if not ok:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=6,
            minSize=(80, 80),
        )

        if len(faces):
            x, y, w, h = max(faces, key=lambda box: box[2] * box[3])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)

            now = time.time()
            if detected_since is None:
                detected_since = now
            elif now - detected_since >= FACE_HOLD_SECONDS:
                face_roi = frame[y : y + h, x : x + w]
                cv2.imwrite(str(SNAPSHOT_PATH), face_roi)

                ser.write(b"SNAPSHOT_READY\n")
                print(f"SNAPSHOT_READY @ {time.strftime('%H:%M:%S')}")
                detected_since = None
        else:
            detected_since = None

        cv2.imshow("WantedScanner", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC om te stoppen
            break
except KeyboardInterrupt:
    pass
finally:
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
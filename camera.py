import time, serial, cv2
from deepface import DeepFace

ESP32_STREAM_URL = "http://172.20.10.8:81/stream"  # replace with Serial monitor IP

cap = cv2.VideoCapture(ESP32_STREAM_URL)

ser = serial.Serial("COM3", 115200, timeout=1)  # pas COM-poort aan
time.sleep(2)  # wacht tot Arduino reset klaar is

frame_idx = 0
try:
    while True:
        ok, raw_frame = cap.read()
        if not ok:
            break
        frame_idx += 1
        if frame_idx % 3:   # sla 2 van de 3 frames over
            continue

        frame = cv2.resize(raw_frame, (320, 240))
        analysis = DeepFace.analyze(
            frame,
            actions=['emotion'],
            detector_backend='opencv',
            enforce_detection=False,
        )

        result = analysis[0] if isinstance(analysis, list) else analysis
        payload = (
            f"{result['emotion']}"

        )
        print(payload.strip())
        ser.write(payload.encode("ascii"))
        cv2.imshow("WantedScanner", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC om te stoppen
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
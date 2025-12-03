import requests
import cv2
import base64

class Interface:
    def __init__(self):
        # Check IP van je Pi!
        self.pi_url = "http://172.20.10.14:5000/update" 

    def _send(self, payload, frame):
        """Hulppunctie om plaatje + data te versturen"""
        if frame is None:
            return

        # 1. Comprimeer het plaatje naar JPG (anders is het te traag over Wifi)
        # quality=50 zorgt voor snelheid, ziet er nog prima uit op klein scherm
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        
        # 2. Maak er een tekst-string van
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        
        # 3. Stop het in de payload
        payload['image'] = jpg_as_text

        try:
            requests.post(self.pi_url, json=payload, timeout=0.2)
        except:
            pass # Negeren als Pi even druk is

    def send_match(self, persoon, frame):
        # Iemand gevonden -> Stuur data + plaatje
        lamp_status = False
        if persoon.danger_level > 80:
            lamp_status = True

        payload = {
            "gevonden": True,
            "naam": persoon.naam,
            "info": f"Leeftijd: {persoon.leeftijd} | Risico: {persoon.danger_level}%",
            "lamp": lamp_status
        }
        self._send(payload, frame)

    def send_reset(self, frame):
        # Niemand gevonden -> Stuur TOCH het plaatje (voor live feed)
        payload = {
            "gevonden": False,
            "lamp": False
        }
        self._send(payload, frame)
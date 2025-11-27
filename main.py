import time

# ---------------------------------------------------------
# HIER IMPORTEER JE JE ANDERE BESTANDEN
# ---------------------------------------------------------
from camera import Camera
from database import Database
from arduino import Arduino
from face import Gezichtsherkenner
from raspberryPi import Interface  # In je UML heet de class RaspberryPi
# Persoon hoef je hier misschien niet te importeren als je hem 
# alleen via de database ontvangt, maar voor type-hinting is het handig:
# from person import Persoon 

class Main:
    def __init__(self):
        print("[MAIN] Systeem initialiseren...")

        # Hier maak je de 'echte' objecten aan vanuit de andere bestanden
        self.cam = Camera()
        self.face = Gezichtsherkenner()
        self.db = Database()
        self.arduino = Arduino()
        self.interface = Interface()

        self.is_running = True

    def run(self):
        # 1. Start verbindingen
        print("[MAIN] Verbinding maken met database...")
        self.db.connection()
        
        print("[MAIN] Systeem is gestart!")

        try:
            while self.is_running:
                # --- STAP 1: KIJKEN ---
                # Haal live frame op uit camera.py
                frame = self.cam.snapshot()

                # --- STAP 2: TONEN ---
                # Toon het huidige beeld in raspberryPi.py zolang er geen gezicht is herkend
                if not gevonden_naam:
                    self.interface.update_live(frame)

                # --- STAP 3: DENKEN ---
                # Vraag aan face.py: "Is dit een gezochte persoon?"
                # Geeft een naam terug of None wanneer geen matchen gezochte persoon?"
                gevonden_naam = self.face.faceScan(frame)

                if gevonden_naam:
                    print(f"[MAIN] Iemand gezien: {gevonden_naam}")
                    
                    # --- STAP 4: DATA OPHALEN ---
                    # Vraag aan database.py: "Geef mij de info van deze naam"
                    persoon_object = self.db.person_on_id(gevonden_naam)

                    if persoon_object:
                        # --- STAP 5: ACTIE ---
                        # Toon de wanted-poster op het Raspberry Pi scherm
                        self.interface.wanted_poster(persoon_object)

                        # Check gevaar en stuur Arduino aan
                        if persoon_object.danger_level > 80:
                            print("[MAIN] GEVAAR! Lamp aan.")
                            self.arduino.lampOn()
                        else:
                            self.arduino.lampOff()
                
                else:
                    # Niemand gezien? Toon live beeld en zorg dat lamp uit is.
                    self.interface.update_live(frame)
                    self.arduino.lampOff()

                # Korte pauze om de processor rust te geven
                time.sleep(0.1)

        except KeyboardInterrupt:
            # Dit gebeurt als je Ctrl+C drukt
            print("\n[MAIN] Stoppen...")
            self.arduino.lampOff()
            print("[MAIN] Tot ziens!")

# Dit zorgt dat het programma start als je op Play drukt
if __name__ == "__main__":
    app = Main()
    app.run()
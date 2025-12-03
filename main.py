import time

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from camera import Camera
from face import Gezichtsherkenner
from raspberryPi import Interface 

# Even uitgezet tot de database werkt:
# from database import Database  

# ---------------------------------------------------------
# MOCK CLASS (TIJDELIJKE VERVANGER VOOR DATABASE)
# ---------------------------------------------------------
class MockPersoon:
    def __init__(self, naam):
        self.naam = naam
        self.leeftijd = 25          # We verzinnen een leeftijd
        self.afkomst = "Nederlands" # We verzinnen een afkomst
        self.danger_level = 85      # Zet dit op 85 om de lamp te testen (boven de 80)

# ---------------------------------------------------------
# MAIN CLASS
# ---------------------------------------------------------
class Main:
    def __init__(self):
        print("[MAIN] Systeem initialiseren (TEST MODUS)...")

        # Objecten aanmaken
        self.cam = Camera()
        self.face = Gezichtsherkenner()
        self.interface = Interface()
        
        # self.db = Database() # Later weer aanzetten

        self.is_running = True

    def run(self):
        # self.db.connection() # Later weer aanzetten
        
        print("[MAIN] Systeem is gestart! Druk Ctrl+C om te stoppen.")

        try:
            while self.is_running:
                # --- STAP 1: KIJKEN ---
                frame = self.cam.snapshot()

                # --- STAP 2: DENKEN (Wie is dit?) ---
                gevonden_naam = self.face.faceScan(frame)

                # --- STAP 3: ACTIE ---
                # ... in de while loop ...
                
                # --- STAP 3: ACTIE ---
                if gevonden_naam:
                    print(f"[MAIN] Iemand gezien: {gevonden_naam}")
                    persoon_object = MockPersoon(gevonden_naam)
                    
                    # GEEF HET FRAME MEE!
                    self.interface.send_match(persoon_object, frame)
                
                else:
                    # GEEF HET FRAME MEE!
                    self.interface.send_reset(frame)

                # Korte pauze om de processor niet op te blazen
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n[MAIN] Stoppen...")
            # Eventueel hier nog een send_reset() sturen om de lamp zeker uit te zetten
            self.interface.send_reset()
            print("[MAIN] Tot ziens!")

if __name__ == "__main__":
    app = Main()
    app.run()
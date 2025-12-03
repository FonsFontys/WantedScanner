from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()  # loads .env into environment variables

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

class Person:
    def __init__(
        self,
        id,
        firstName,
        lastName,
        age,
        eyeColour,
        gender,
        features,
        dangerLevel,
        soughtBy,
        image=None #currently none for testing due to no image being in database

    ):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.eyeColour = eyeColour
        self.gender = gender
        self.features = features
        self.dangerLevel = dangerLevel
        self.soughtBy = soughtBy
        self.image = image

def get_all_people():
    people = []
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, Voornaam, Achternaam, Leeftijd, Oogkleur, Geslacht, 
                   Belangrijke_kenmerken, Gevaarlijkheid_niveau, Gezocht_door
            FROM database_gegevens
        """)#add ", image" after gezocht_door when there are images in the database
        rows = cursor.fetchall()
        people = [Person(*row) for row in rows]
    except mysql.connector.Error as e:
        print("DB Error:", e)
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    return people
class Database:
    def __init__(self):
        self.people = get_all_people()
        self.people_dict = {p.id: p for p in self.people}

    def person_on_id(self, id):
        return self.people_dict.get(id)

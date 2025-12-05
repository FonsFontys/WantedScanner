from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables
load_dotenv()

# Database config
DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

# Folder to save images
IMAGE_FOLDER = "ReferencePhotos"
os.makedirs(IMAGE_FOLDER, exist_ok=True)  # create if missing


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
        image=None  # path to saved image
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
        self.image = image  # string path to image file


def save_image_file(person_id, image_blob):
    """Saves image BLOB to disk and returns its path."""
    if image_blob is None:
        return None

    file_path = os.path.join(IMAGE_FOLDER, f"{person_id}.jpg")
    try:
        with open(file_path, "wb") as f:
            f.write(image_blob)
        return file_path
    except Exception as e:
        print(f"Error saving image for ID {person_id}: {e}")
        return None


def get_all_people():
    """Fetch all people from the DB and save their images locally."""
    people = []
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, Voornaam, Achternaam, Leeftijd, Oogkleur, Geslacht, 
                   Belangrijke_kenmerken, Gevaarlijkheid_niveau, Gezocht_door, image
            FROM database_gegevens
        """)
        rows = cursor.fetchall()

        for row in rows:
            (id, first, last, age, eye, gender, features,
             danger, soughtBy, image_blob) = row

            # Save image and get local path
            image_path = save_image_file(id, image_blob)

            person = Person(
                id, first, last, age, eye, gender,
                features, danger, soughtBy, image_path
            )
            people.append(person)

    except mysql.connector.Error as e:
        print("DB Error:", e)
    finally:
        try:
            cursor.close()
            db.close()
        except:
            pass

    return people


class Database:
    def __init__(self):
        self.people = get_all_people()
        self.people_dict = {p.id: p for p in self.people}

    def person_on_id(self, id):
        return self.people_dict.get(id)

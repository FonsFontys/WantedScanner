import serial
import mysql.connector
import time


DB_CONFIG = { # fill these values in with the values from the database
    'host': 'SQLserver',
    'user': 'WANTEDSCANNER\Administrator',
    'password': 'Admin123',
    'database': '' 
}

db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()


try:
    while True:
        if #get the data from main

            parts = line.split() #what to split on depends on how the input is formulated

            Age = parts[0]
            Gender = parts[1]
            Emotion = parts[2]
            Race = parts[3]
            query = """
                        INSERT INTO `test_schema`(Leeftijd, Geslacht, Emotie, Ras)
                        VALUES (%s, %s, %s, %s)
                    """ #TableName still needs to be changed
            #image will be send seperatly
            cursor.execute(query, (Age, Gender, Emotion, Race))
            db.commit()
        else:
            time.sleep(2) #check every 2 seconds
except KeyboardInterrupt: #use CTRL + C to stop the program
    print("\nStopped by user.")
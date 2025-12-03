# main.py
from main import Database

# Get all people from the database

people = Database().people

# Test: print first 5 people
print(f"Total people fetched: {len(people)}\n")
for i, person in enumerate(people[:5]):
    print(f"Person {i+1}:")
    print(f"  ID: {person.id}")
    print(f"  Name: {person.firstName} {person.lastName}")
    print(f"  Age: {person.age}")
    print(f"  Eye Colour: {person.eyeColour}")
    print(f"  Gender: {person.gender}")
    print(f"  Features: {person.features}")
    print(f"  Danger Level: {person.dangerLevel}")
    print(f"  Sought By: {person.soughtBy}")
    print(f"  Image: {person.image}")
    print("-" * 40)

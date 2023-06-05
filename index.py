import requests
import math
import pymongo
from bson import DBRef

# Load starships from API into the variable 'starships'
number_of_starships = requests.get('https://swapi.dev/api/starships').json()['count']
starships_per_page = len(requests.get('https://swapi.dev/api/starships').json()['results'])
starships = []
for i in range(1, (math.ceil(number_of_starships / starships_per_page)) + 1):
    starships_on_page = requests.get(f'https://swapi.dev/api/starships?page={i}').json()['results']
    for starship in starships_on_page:
        starships.append(starship)

client = pymongo.MongoClient()
db = client['starwars']

# Replace starship pilot names with 'object_id' from starwars.characters
for starship in starships:
    if len(starship['pilots']) > 0:
        for i in range(0, len(starship['pilots'])):
            name_of_pilot = requests.get(f"{starship['pilots'][i]}").json()['name']
            pilot_object_id_in_db = str(db.characters.find_one({'name': name_of_pilot})['_id'])
            starship['pilots'][i] = DBRef('characters', pilot_object_id_in_db) #{"$oid": f"{pilot_object_id_in_db}"}

# Create the collection 'starships' in the starwars data cluster
try:
    db.create_collection('starships')
    db.starships.insert_many(starships)
except pymongo.errors.CollectionInvalid:
    print("Collection 'starships' already exists...")
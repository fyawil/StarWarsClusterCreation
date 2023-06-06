import requests
import math
import pymongo
from bson import DBRef


def get_starships(api):
    '''Load starships from API into the variable 'starships' as a list'''
    number_of_starships = requests.get(api).json()['count']
    starships_per_page = len(requests.get(api).json()['results'])
    no_of_pages_to_get_from_api = math.ceil(number_of_starships / starships_per_page)

    starships = []

    for i in range(1, no_of_pages_to_get_from_api + 1):
        starships_on_page = requests.get(f'{api}?page={i}').json()['results']
        for starship in starships_on_page:
            starships.append(starship)

    return starships

def connect_to_db(db_name):
    client = pymongo.MongoClient()
    db = client[f"{db_name}"]
    return db

def get_pilot_ref(db, name_of_pilot):
    return str(db.characters.find_one({'name': name_of_pilot})['_id'])

def replace_api_urls_with_db_ref(starships, db):
    '''Replace starship pilot names with 'object_id' from starwars.characters'''
    for starship in starships:

        if len(starship['pilots']) <= 0:
            continue

        for i in range(0, len(starship['pilots'])):

            name_of_pilot = requests.get(f"{starship['pilots'][i]}").json()['name']
            pilot_object_id_in_db = get_pilot_ref(db, name_of_pilot)

            starship['pilots'][i] = DBRef('characters', pilot_object_id_in_db)

def create_cluster_in_db(source_of_collection, name_of_cluster, db):
    '''Create the collection 'starships' in the starwars data cluster'''

    try:
        db.create_collection(f"{name_of_cluster}")
        db.starships.insert_many(source_of_collection)

    except pymongo.errors.CollectionInvalid:
        print(f"Collection {name_of_cluster} already exists...")


if __name__ == '__main__':
    starships = get_starships('https://swapi.dev/api/starships')
    db = connect_to_db('starwars')

    replace_api_urls_with_db_ref(starships, db)

    create_cluster_in_db(starships, 'starships', db)
import unittest
import requests
import pymongo
from bson import DBRef

from index import (
    get_starships,
    connect_to_db,
    get_pilot_ref,
    replace_api_urls_with_db_ref,
    create_cluster_in_db
)

class StarshipsTestCase(unittest.TestCase):

    def setUp(self):
        self.test_api = 'https://swapi.dev/api/starships'
        self.test_db_name = 'test_db'
        self.test_db = pymongo.MongoClient()[self.test_db_name]

    def tearDown(self):
        self.test_db.drop_collection('starships')

    def test_get_starships(self):
        starships = get_starships(self.test_api)
        self.assertIsInstance(starships, list)
        self.assertTrue(len(starships) > 0)

    def test_connect_to_db(self):
        db = connect_to_db(self.test_db_name)
        self.assertIsInstance(db, pymongo.database.Database)
        self.assertEqual(db.name, self.test_db_name)

#     def test_get_pilot_ref(self):
#         # Create a test document in the database
#         pilots = [{'name': 'Luke Skywalker'}]
#         pilot_id = self.test_db.characters.insert_one(pilots).inserted_id

#         # Test getting the id of pilot
#         pilot_ref = get_pilot_ref(self.test_db, 'Luke Skywalker')
#         expected_ref = str(pilot_id)
#         self.assertEqual(pilot_ref, expected_ref)

#     # def test_replace_api_urls_with_db_ref(self):
#     #     # Create test starships and pilots
#     #     starships = [
#     #         {'name': 'Starship 1', 'pilots': ['https://swapi.dev/api/people/1']},
#     #         {'name': 'Starship 2', 'pilots': ['https://swapi.dev/api/people/2']},
#     #         {'name': 'Starship 3', 'pilots': []}
#     #     ]
#     #     pilots = [
#     #         {'name': 'Luke Skywalker'}, # f"{requests.get('https://swapi.dev/api/people/1').json()['name']}"},
#     #         {'name': 'Chewbacca'} #f"{requests.get('https://swapi.dev/api/people/2').json()['name']}"}
#     #     ]

#     #     # Insert test pilots into the database
#     #     self.test_db.characters.insert_many(pilots)

#     #     # Replace API URLs with DBRef
#     #     replace_api_urls_with_db_ref(starships, self.test_db)

#     #     # Test if the pilots were replaced correctly
#     #     expected_starships = [
#     #         {'name': 'Starship 1', 'pilots': DBRef('characters', [self.test_db.characters.find_one({'name': 'Luke Skywalker'})['_id']])},
#     #         {'name': 'Starship 2', 'pilots': DBRef('characters', [self.test_db.characters.find_one({'name': 'Chewbacca'})['_id']])},
#     #         {'name': 'Starship 3', 'pilots': []}
#     #     ]
#     #     self.assertEqual(starships, expected_starships)

#     # def test_create_cluster_in_db(self):
#     #     # Create test starships
#     #     starships = [
#     #         {'name': 'Starship 1'},
#     #         {'name': 'Starship 2'},
#     #         {'name': 'Starship 3'}
#     #     ]

#     #     # Create the cluster in the test database
#     #     create_cluster_in_db(starships, 'starships', self.test_db)

#     #     # Check if the collection was created and documents were inserted
#     #     self.assertIn('starships', self.test_db.list_collection_names())
#     #     self.assertEqual(self.test_db.starships.count_documents({}), len(starships))


if __name__ == '__main__':
    unittest.main()

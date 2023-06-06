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

if __name__ == '__main__':
    unittest.main()

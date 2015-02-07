import os
import json
import app
import config
import unittest
from mongoengine import connect
from pymongo import MongoClient
client = MongoClient()


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config["MONGODB_DB"] = 'dfkm'
        connect(
            config.MONGO_DBNAME,
            host=config.MONGO_HOST,
            port=config.MONGO_PORT
        )
        self.app = app.app.test_client()
        self.name = app.app.name
        
    def tearDown(self):
        
        db = client[self.name]
        client.drop_database(self.name)

    def test_index_call(self):
        response = self.app.get('/')
        print response

    def test_POST_simple_point(self):
        
        data = {'zone_name' : 'test zone',
                'description' : 'new dangerous zone',
                'loc' : {'type' : 'Point',
                         'coordinates': [ 40, 5 ]},
                'radius': 10,
                }
        
        data = json.dumps(data)
        
        res = self.app.post('/api/v1.0/zones',
                             data=data,
                             content_type='application/json')
        db = client[self.name]
        coll = db['zones']
        res = coll.count()
        assert res == 1
        

if __name__ == '__main__':
    unittest.main()
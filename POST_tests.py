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
        #app.app.config["MONGODB_DB"] = 'dfkm'
        connect(
            config.MONGO_DBNAME,
            host=config.MONGO_HOST,
            port=config.MONGO_PORT
        )
        self.app = app.app.test_client()
        
    def tearDown(self):
        return None

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
        db = client['dfkm']
        coll = db['zones']
        res = coll.find()
        for x in res:
            print x
        
    #def test_get(self):
        

        
        

if __name__ == '__main__':
    unittest.main()
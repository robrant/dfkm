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
        
        # Setup the database (index build, etc)
        app.init_db()
        
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

    def test_POST_simple_polygon(self):
        
        data = {'zone_name' : 'test zone polygon',
                'description' : 'new dangerous polygon zone',
                'loc' : {'type' : 'Polygon',
                         'coordinates': [ [ [ 0 , 0 ] , [ 3 , 6 ] , [ 6 , 1 ] , [ 0 , 0  ] ] ]}
                }
        
        data = json.dumps(data)
        
        res = self.app.post('/api/v1.0/zones',
                             data=data,
                             content_type='application/json')
        db = client[self.name]
        coll = db['zones']
        assert coll.count() == 1

        res = coll.find()
        print res


    def test_GET_simple_point(self):
        
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
        
        response = self.app.get('/api/v1.0/getzones')
        for x in response:
            print x
        
if __name__ == '__main__':
    unittest.main()
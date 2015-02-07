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
    
    def test_user_enter(self):
        """ Checks that user enter adds to the db correctly """
        
        # Horrid hack to generate a zone
        data = {'zone_name' : 'test zone polygon',
                'description' : 'new dangerous polygon zone',
                'loc' : {'type' : 'Polygon',
                         'coordinates': [ [ [ 0 , 0 ] , [ 3 , 6 ] , [ 6 , 1 ] , [ 0 , 0  ] ] ]}}
        res = self.app.post('/api/v1.0/zones', data=json.dumps(data), content_type='application/json')
        zone_id = json.loads(res.data)['zone_id']
        
        # Hit the API and get back a user who entered        
        url = '/api/v1.0/enter/%s' %(zone_id)
        get_res = self.app.get(url)
        user_id = json.loads(get_res.data)['user_id']

        assert len(user_id) == 24

        # Check it's in the db too
        db = client[self.name]
        coll = db['users']
        assert coll.count() == 1
        
        
    def test_user_exit(self):
        """ Checks that user gets deleted from the db when exiting """
        
        # Horrid hack to generate a zone
        data = {'zone_name' : 'test zone polygon',
                'description' : 'new dangerous polygon zone',
                'loc' : {'type' : 'Polygon',
                         'coordinates': [ [ [ 0 , 0 ] , [ 3 , 6 ] , [ 6 , 1 ] , [ 0 , 0  ] ] ]}}
        res = self.app.post('/api/v1.0/zones', data=json.dumps(data), content_type='application/json')
        zone_id = json.loads(res.data)['zone_id']
        
        # Hit the API and get back a user who entered        
        url = '/api/v1.0/enter/%s' %(zone_id)
        get_res = self.app.get(url)
        user_id = json.loads(get_res.data)['user_id']

        # Hit the API and get back a user who entered        
        url = '/api/v1.0/exit/%s/%s' %(str(zone_id), str(user_id))
        get_res = self.app.get(url)
        
        # Now check that the db doens't contain the user
        db = client[self.name]
        coll = db['users']
        docs = coll.find()
        
        assert docs[0]['active'] == False
        
    def test_GET_user_count_for_zone(self):
        """ Gets the number of users in a zone"""
        
        # Horrid hack to generate a zone
        data = {'zone_name' : 'test zone polygon',
                'description' : 'new dangerous polygon zone',
                'loc' : {'type' : 'Polygon',
                         'coordinates': [ [ [ 0 , 0 ] , [ 3 , 6 ] , [ 6 , 1 ] , [ 0 , 0  ] ] ]}}
        res = self.app.post('/api/v1.0/zones', data=json.dumps(data), content_type='application/json')
        zone_id = json.loads(res.data)['zone_id']
        
        for i in range(10):
        
            # Hit the API and get back a user who entered        
            url = '/api/v1.0/enter/%s' %(zone_id)
            get_res = self.app.get(url)
            user_id = json.loads(get_res.data)['user_id']
    
            # Hit the API and get back a user who entered        
            if i % 2 == 0:
                url = '/api/v1.0/exit/%s/%s' %(str(zone_id), str(user_id))
                get_res = self.app.get(url)
        
        # Now check that the db doens't contain the user
        db = client[self.name]
        coll = db['users']
        docs = coll.find()
        
        assert coll.count() == 10
        
        # Get the count from the API
        url = '/api/v1.0/user_count/%s' %(zone_id)
        count_response = self.app.get(url)
        
        assert json.loads(count_response.data)['user_count'] == 5

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
        
                
if __name__ == '__main__':
    unittest.main()
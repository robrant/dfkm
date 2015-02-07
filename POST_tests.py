import os
import app
import config
import unittest
from mongoengine import connect

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config["MONGODB_DB"] = 'xxx'
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

if __name__ == '__main__':
    unittest.main()
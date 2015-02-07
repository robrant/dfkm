#curl -XPOST 'http://ec2-54-77-57-184.eu-west-1.compute.amazonaws.com:5000//api/v1.0/zones/

import requests
import json

data = {'zone_name' : 'Lansdown',
                'description' : 'Danger, danger, danger',
                'loc' : {'type' : 'Point',
                         'coordinates': [ -1.866, 50.722 ]},
                'radius': 50,
                }

headers = {'content-type': 'application/json'}

r = requests.post("http://ec2-54-77-57-184.eu-west-1.compute.amazonaws.com:5000/api/v1.0/zones", data=json.dumps(data), headers=headers)

print r.content
print r.status_code
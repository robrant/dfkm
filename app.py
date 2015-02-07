
from flask import Flask, render_template, jsonify, request, Response
from flask import abort
from flask import Response
from pymongo import GEOSPHERE
import json

from flask.ext.pymongo import PyMongo
from config import MONGO_DBNAME, MONGO_PORT
import json

app = Flask('dfkm')
mongo = PyMongo(app, config_prefix='MONGO')

app.debug = True
app.config['SECRET_KEY'] = 'secret!'


# -----------------------------------------------------------------------------

def init_db():
    """ Placeholder for initialising the database"""

    # Put a spatial index on the loc field
    with app.app_context():
        mongo.db.zones.ensure_index( [("loc",GEOSPHERE)] )

@app.route('/')
def index():
    """ normal http request to a serve up the page """
    return jsonify({"hello":"world"})


@app.route('/makezone')
def makezone():
    """ normal http request to a serve up the page """
    return render_template('index.html')



def updateRisk():
    #Get the zones
    rec = mongo.db.zones.find()
    for r in rec:
        #do a geo within query for the accidents data
        coords = r['loc']['coordinates']
        #Radius of earth in meters - to convert to radians for mongo
        radius = r['radius']/6378100
        numAcc = mongo.db.accidents.find( {'geometry': { '$geoWithin': { '$centerSphere': [ coords, radius ] } }} ).count()
        upd = mongo.db.zones.update({'_id':r['_id']}, {'$set': {"risk": numAcc}})
        print upd, numAcc, radius
    print 'updated'


@app.route('/api/v1.0/getzones', methods=['GET'])
def getzones():
    """ Grabbing and returning the zones """

    #Update the risk vals
    updateRisk()

    data = request.args.get('zone_name', None)
    print data
    #Check if data is null - get all zones
    out = []
    if data:
        rec = mongo.db.zones.find({'zone_name':data})
    else:
        rec = mongo.db.zones.find()
    for r in rec:
        r.pop('_id')
        out.append(r)

    jsonOut = json.dumps(out)

    return Response(response=jsonOut,
                    status=200,
                    mimetype="application/json")


@app.route('/api/v1.0/zones', methods=['POST'])
def create_zone():

    # Setup a zone object to insert
    zone = {}

    # Ensure post's Content-Type is supported
    if request.headers['content-type'] == 'application/json':
        # Ensure data is a valid JSON
        try:
            content = json.loads(request.data)
        except ValueError:
            return Response(status=405)

    # GEO INPUT
    try:
        loc = content['loc']
        zone['loc'] = loc

    except:
        return Response(status=405)

    # HANDLE POINT DATA
    if loc['type'].lower() == 'point' and content.has_key('radius') == True:
        zone['radius'] = content['radius']

    # HANDLE POLYGON DATA
    if loc['type'].lower() == 'polygon':
        zone['loc'] = loc

    # Default on the risk score
    if content.has_key('risk') == True:
        zone['risk'] = content['risk']
    else:
        zone['risk'] = 0

    # Default on the zone name
    if content.has_key('zone name') == True:
        zone['zone_name'] = content['zone_name']
    else:
        zone['zone_name'] = 'placeholder for zone name'

    # Description
    if content.has_key('description') == True:
        zone['description'] = content['description']
    else:
        zone['description'] = 'new zone'

    # Now push to mongo
    zone_id = mongo.db.zones.insert(zone)

    if len(str(zone_id)) == 24:
        response = {'zone_id' : str(zone_id) }

    return jsonify(response), 201


if __name__ == '__main__':
    """
    Run the server
    """

    app.run(host='0.0.0.0', port=5000, debug=True)

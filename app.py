
from flask import Flask, render_template, jsonify, request
from flask import abort

from flask.ext.pymongo import PyMongo
from config import MONGO_DBNAME, MONGO_PORT

app = Flask(__name__)
mongo = PyMongo(app, config_prefix='MONGO')

app.debug = True
app.config['SECRET_KEY'] = 'secret!'

# -----------------------------------------------------------------------------

@app.route('/')
def index():
    """ normal http request to a serve up the page """
    return render_template('index.html')



@app.route('/api/v1.0/getzones', methods=['GET'])
def getzones():
    """ Grabbing and returning the zones """
    if not request.json:
        abort(400)
    else:
        data = request.args.get('zone_name', None)
        print data
        #Check if data is null - get all zones
        if data:
            rec = mongo.dfkm.zones.find({'zone_name':data})
        else:
            rec = mongo.dfkm.zones.find()
        return jsonify(rec)


@app.route('/api/v1.0/zones', methods=['POST'])
def create_zone():

    if not request.json:
        abort(400)
    else:
        loc = request.json['loc']
        loc_type = request.json['loc_type']

    zone = {
            'zone_name': request.json['zone_name'],
            'description': request.json.get('description', ""),
            'loc' : loc,
            #'risk' : PLACEHOLDER FOR GETTING THE RISK SCORE
    }

    # Now push to mongo


    #return jsonify({'zone_id': zone_id}), 201


if __name__ == '__main__':
    """
    Run the server
    """

    app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, render_template, jsonify, request
from flask import abort

from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

app.debug = True
app.config['SECRET_KEY'] = 'secret!'

# -----------------------------------------------------------------------------

@app.route('/')
def index():
    """ normal http request to a serve up the page """
    return render_template('index.html')



@app.route('/api/v1.0/getzones')
def getzones():
    """ Grabbing and returning the zones """
    data = request.args.get('zid', None)
    print data
    rec = mongo.db.people.update({'name':d['name']},
                                  {'$set': { 'Vis':int(data[0]),
                                            'Stats':int(data[1]),
                                            'Coding':int(data[2]),
                                            'Comms':int(data[3]),
                                            'Domain Exp':int(data[4])}})



    return render_template('index.html')




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


    return jsonify({'zone_id': zone_id}), 201


if __name__ == '__main__':
    """
    Run the server
    """

    app.run(host='0.0.0.0', port=80, debug=True)

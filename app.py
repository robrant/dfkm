
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
    return jsonify({"hello":"world"})


@app.route('/api/v1.0/zones', methods=['POST'])
def create_zone():
    
    if not request.json:
        abort(400)
    zone = {
            'zone_name': request.json['zone_name'],
            'description': request.json.get('description', ""),
            'loc' : {''}
    }
    
    # Now push to mongo
    
    
    return jsonify({'zone_id': zone_id}), 201

if __name__ == '__main__':
    """
    Run the server
    """

    app.run(host='0.0.0.0', port=80, debug=True)
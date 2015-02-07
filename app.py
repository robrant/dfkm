
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

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
    return render_template('index.html')



if __name__ == '__main__':
    """
    Run the server
    """

    app.run(host='0.0.0.0', port=5000, debug=True)
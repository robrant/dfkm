
from flask import Flask, render_template, jsonify

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'secret!'

# -----------------------------------------------------------------------------

@app.route('/')
def index():
    """ normal http request to a serve up the page """  
    return jsonify({"hello":"world"})


if __name__ == '__main__':
    """
    Run the server
    """

    app.run(host='0.0.0.0', port=5000, debug=True)
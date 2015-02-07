
from flask import Flask, render_template

app = Flask(__name__)

app.config.update(
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = '27017',
    MONGODB_DB = 'dfkm',
)

app.debug = True
app.config['SECRET_KEY'] = 'secret!'

# -----------------------------------------------------------------------------

@app.route('/')
def index():
    """ normal http request to a serve up the page """  
    return render_template('index.html')


if __name__ == '__main__':
    """
    Run the server
    """

    app.run(host='0.0.0.0', port=8080, debug=True)
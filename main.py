import flask
import waitress

app = flask.Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    return flask.render_template("index.html")

waitress.serve(app, host='127.0.0.1', port=3002)


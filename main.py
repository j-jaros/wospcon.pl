import flask
import waitress

app = flask.Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    return flask.render_template("index.html")


app.run(host='0.0.0.0', port=80)
#waitress.serve(app, host='0.0.0.0', port=80, debug=True)


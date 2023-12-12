import flask
import waitress

app = flask.Flask(__name__, static_url_path='/static')


@app.errorhandler(404)
def reroute_to_index():
    return flask.redirect("/")


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/documents/<docname>")
@app.route("/documents")
@app.route("/documents/")
def documents(docname=None):
    if docname is None:
        return flask.redirect("/")
    else:
        try:
            return flask.send_from_directory("./documents/", f"./{docname}")
        except Exception as ex:
            return "Plik nie istnieje. Przepraszamy!"


waitress.serve(app, host='0.0.0.0', port=3002)

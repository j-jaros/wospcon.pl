import threading

import flask
import pymysql
import waitress
import werkzeug.exceptions

app = flask.Flask(__name__, static_url_path='/static', )


@app.errorhandler(404)
def notfound_handler(e):
    if flask.request.method != "GET":
        return flask.jsonify('Zasob nie zostal znaleziony')

    return flask.render_template("404.html")


@app.errorhandler(405)
def methodunallowed_handler(e):
    if flask.request.method != "GET":
        return flask.jsonify(f'Metoda {flask.request.method} jest niedozwolona')

    return flask.render_template("405.html")


@app.errorhandler(500)
def internalerror_handler(e):
    if flask.request.method != "GET":
        return flask.jsonify(f'Wystąpił błąd serwera.')

    return flask.render_template("500.html")


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
            raise werkzeug.exceptions.NotFound


connection = None
cursor = None


def connect_to_database():
    global connection
    global cursor

    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user='root',
        password='root',
        database='wospcon'
    )
    cursor = connection.cursor()


threading.Thread(target=connect_to_database).start()

waitress.serve(app, host='0.0.0.0', port=3002)

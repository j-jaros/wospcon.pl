import base64
import threading
import time
import traceback

import flask
import pymysql
import waitress
import werkzeug.exceptions

app = flask.Flask(__name__, static_url_path='/static', )


@app.errorhandler(404)
def notfound_handler(e):
    log(flask.request, 'error', args=str(e))
    if flask.request.method != "GET":
        return flask.jsonify('Zasob nie zostal znaleziony')

    return flask.render_template("404.html")


@app.errorhandler(405)
def methodunallowed_handler(e):
    log(flask.request, 'error', args=str(traceback.format_exc()))
    if flask.request.method != "GET":
        return flask.jsonify(f'Metoda {flask.request.method} jest niedozwolona')

    return flask.render_template("405.html")


@app.errorhandler(500)
def internalerror_handler(e):
    log(flask.request, 'error', args=str(traceback.format_exc()))
    if flask.request.method != "GET":
        return flask.jsonify(f'Wystąpił błąd serwera.')

    return flask.render_template("500.html")


@app.route("/")
def index():
    log(flask.request, 'page-access')
    return flask.render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return 'nie ma favicona :)'


@app.route("/documents/<docname>")
@app.route("/documents")
@app.route("/documents/")
def documents(docname=None):
    log(flask.request, 'document-access', args=str(docname))
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

    try:
        connection = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user='root',
            password='',
            database='wospcon'
        )
        cursor = connection.cursor()
        connection.autocommit(True)
    except Exception as ex:
        print(f"{time.time()} Nie mozna polaczyc do bazy danych: {ex}")
        connection = None
        cursor = None


def log(req_obj, type, args=None):
    print(f"[{time.time()}] IP: {req_obj.host} | TYPE: {type} | ARGS: {args}")
    try:
        if connection is None or cursor is None:
            return

        socket = req_obj.host
        sanitized_args = base64.b64encode(bytes(str(args), 'utf-8'))
        cursor.execute("insert into entry_log (id, socket, type, time, args) values (%s,%s,%s,%s, %s)",
                       (0, socket, type, time.time(), sanitized_args if args is not None else None))
    except Exception as ex:
        print(f"{time.time()} Nie mozna zapisac loga: {ex}")


threading.Thread(target=connect_to_database).start()

waitress.serve(app, host='0.0.0.0', port=3002)

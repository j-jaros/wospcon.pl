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
    log(flask.request, 'resource-not-found', args=str(flask.request.url))
    if flask.request.method != "GET":
        return flask.jsonify('Zasob nie zostal znaleziony')

    return flask.render_template("404.html")


@app.errorhandler(405)
def methodunallowed_handler(e):
    log(flask.request, 'unallowed-method', args=str(traceback.format_exc()))
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
    return flask.send_from_directory("./static", "favicon.png")


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


logs = []


def dump_logs():
    while True:
        time.sleep(5)
        print(logs)
        log_len = len(logs)
        if log_len != 0:
            try:
                if connection is None or cursor is None:
                    pass
                else:
                    cursor.executemany("insert into entry_log (id, socket, type, time, args) values (0 ,%s,%s,%s,%s)",
                                       logs)

                    # logi usuwam w ten sposob dla pewnosci ze nie usune loga ktory jeszcze nie zostal zapisany do bazy danych
                    del logs[0:log_len]
            except Exception as ex:
                print(f"{time.time()} Nie mozna zapisac loga: {ex}")


def log(req_obj, type, args=None):
    sanitized_args = None
    if args is not None:
        sanitized_args = base64.b64encode(bytes(str(args), 'utf-8'))

    socket = req_obj.access_route[-1]

    print(f"[{time.time()}] IP: {socket} | TYPE: {type} | ARGS: {args}")
    logs.append((socket, type, time.time(), sanitized_args))


threading.Thread(target=connect_to_database).start()
threading.Thread(target=dump_logs).start()

waitress.serve(app, host='0.0.0.0', port=3002)

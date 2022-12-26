import flask
import json
import time
import random
import base64
from websocket import create_connection
from jewcord_db import jewcord_db

wss = [create_connection("wss://Chat-Websockets.sachsthebased.repl.co")]

appie = flask.Blueprint('api', __name__, template_folder='templates')

jewcord_db = jewcord_db()


@appie.route('/api/v1/chats/<server>/<channel>/messages', methods=['GET', 'POST'])
def messages_api(server: int, channel: int):
    if flask.request.method == "GET":
        channels = jewcord_db.find_server_channels(server)
        channel = jewcord_db.find_channel(channels, channel)

        res = flask.Response(response=json.dumps({"messages": channel["messages"]}), status=200, mimetype='application/json')
        return res

    elif flask.request.method == "POST":
        req = flask.request.get_json(force=True)
        data = {
            "timestamp": time.time(),
            "content": req["content"],
            "embeds": req["embeds"],
            "files": req["files"],
            "author": jewcord_db.get_user("token", flask.request.headers["tokens"])
        }
        jewcord_db.new_message(server, channel, data)


@appie.route('/api/v1/login', methods=['POST'])
def login():
    if flask.request.method == "POST":
        req = flask.request.get_json(force=True)
        log = jewcord_db.login(req["email"], req["password"])
        if log is not False:
            res = flask.Response(response=json.dumps({"token": log}), status=200, mimetype='application/json')
            return res
        else:
            res = flask.Response(response=json.dumps({"token": "Bad Password"}), status=401, mimetype='application/json')
            return res


@appie.route('/api/v1/signup', methods=['POST'])
def signup():
    if flask.request.method == 'POST':
        req = flask.request.get_json(force=True)
        sign = jewcord_db.new_user(req["email"], req["name"], req["password"])

        if sign is False:
            res = flask.Response(response=json.dumps({"token": "Something went fuck"}), status=400, mimetype='application/json')
            return res
        res = flask.Response(response=json.dumps({"token": sign}), status=200, mimetype='application/json')
        return res


@appie.route('/api/v1/users/<id>', methods=['GET', 'PATCH'])
def user_api(id):
    if id == "@me":
        user = jewcord_db.get_user("token", flask.request.headers["token"])
    else:
        user = jewcord_db.get_user("id", id)

    res = flask.Response(response=json.dumps(user), status=200, mimetype='application/json')
    return res

@appie.route('/api/v1/servers/<id>', methods=['GET', 'DELETE', 'PATCH'])
def server_api(id):
    if flask.request.method == 'GET':
        pass

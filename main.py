import flask
from appie import appie
from views import views
from jewcord_db import jewcord_db

app = flask.Flask('app')
app.register_blueprint(appie)
app.register_blueprint(views)

"""
db["servers"]["0"]["members"].append(
  {"name": "gruppe sechs",  "tag": 1, "id": 14306021050429760677, "nickname": None, "roles": []}
)
"""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, threaded=True)

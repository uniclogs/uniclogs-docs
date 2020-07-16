import log_interface
from endpoints.passes import *
from loguru import logger
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


def initDb(user, password, db, app, host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


log_interface.init(__name__)
app = Flask(__name__)

initDb('postgres', '069790153', 'capst', app)   # TODO read credentials from environment
db = SQLAlchemy(app)

# setup endpoints
api = Api(app)
api.add_resource(Passes, '/passes')



def run():
    app.run(debug=True)

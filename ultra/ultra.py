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



def run():
    log_interface.init(__name__)
    app = Flask(__name__)

    initDb('postgres', '069790153', 'capst', app)   # DB credentials hard-coded for now. It is planned moving it to a configuration file
    db = SQLAlchemy(app)

    # setup endpoints
    api = Api(app)
    api.add_resource(Passes, '/passes')

    app.run(debug=True)

import log_interface
from api_resources import *
from loguru import logger
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import sys



def initDb(user, password, db, host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


log_interface.init(__name__)
app = Flask(__name__)

initDb('postgres', '069790153', 'capst')   # DB credentials hard-coded for now. It is planned moving it to a configuration file
db = SQLAlchemy(app)

api = Api(app)
api.add_resource(HelloWorld, '/')


def run():
    app.run(debug=True)

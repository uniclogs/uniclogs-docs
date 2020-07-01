import log_interface
from api_resources import *
from loguru import logger
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

class Ultra:
    def __init__(self):
        self.logger = log_interface.init(__name__)
        self.app = Flask(__name__)
        self.initDb('postgres', '', 'capst')   # DB credentials hard-coded for now. It will moved to a configuration file


        self.api = Api(self.app)
        self.api.add_resource(HelloWorld, '/')

    def initDb(self, user, password, db, host='localhost', port=5432):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = url
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
        self.db = SQLAlchemy(self.app)
        self.db.engine.execute(text("SELECT 1")) #Check connection is


    def run(self):
        self.app.run(debug=True)

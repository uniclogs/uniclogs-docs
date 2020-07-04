import log_interface
from endpoints.passes import *
from loguru import logger
from flask import Flask
from flask_restful import Api


class Ultra:
    def __init__(self):
        self.logger = log_interface.init(__name__)
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Passes, '/passes')

    def run(self):
        self.app.run(debug=True)


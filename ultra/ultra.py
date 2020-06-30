import log_interface
from api_resources import *
from loguru import logger
from flask import Flask
from flask_restful import Api



def main():
    log_interface.init("api")

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(HelloWorld, '/')
    app.run(debug=True)

if __name__ == "__main__":
    main()

import log_interface
from endpoints import PassesEndpoint, RequestEndpoint, RequestIdEndpoint
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from database import db, init_db

import sys
sys.path.insert(0, '..')
import pass_calculator as pc


log_interface.init(__name__)
app = Flask(__name__)
api = Api(app)


# add OrbitalPass json encoder to app
app.config["RESTFUL_JSON"] = {
        "separators": (", ", ": "),
        "indent": 2,
        "cls": pc.orbitalpass.OrbitalPassJsonEncoder
}


# setup endpoints
api.add_resource(PassesEndpoint, '/passes')
api.add_resource(RequestEndpoint, '/request')
api.add_resource(RequestIdEndpoint, '/request/<int:request_id>')


def run():
    init_db(app)
    app.run(debug=True)

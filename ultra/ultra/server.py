import flask_restful as fr
import flask
from flask_cors import CORS
import ultra.database as db
import ultra.log_interface as li
import ultra.endpoints.passes as passes
import ultra.endpoints.request as request
import ultra.endpoints.request_id as request_id
import ultra.endpoints.user as user
import ultra.endpoints.signal as signal
import ultra.endpoints.telemetry as telemetry
import pass_calculator as pc

"""
Programer Loader
This class emits a connection to the PgSQL database
Then initializes the Flask back-end server and set up REST endpoints
"""


li.init(__name__)
app = flask.Flask(__name__)
CORS(app)
api = fr.Api(app)


# add OrbitalPass json encoder to app
app.config["RESTFUL_JSON"] = {
        "separators": (", ", ": "),
        "indent": 2,
        "cls": pc.orbitalpass.OrbitalPassJsonEncoder
}


# Setup the Flask endpoints
api.add_resource(passes.PassesEndpoint, '/passes')
api.add_resource(request.RequestEndpoint, '/request')
api.add_resource(request_id.RequestIdEndpoint, '/request/<int:request_id>')
api.add_resource(user.UserEndpoint, '/user')
api.add_resource(signal.SignalEndpoint, '/signal')
api.add_resource(telemetry.TelemetryEndpoint, '/telemetry')


def run():
    db.init_db(app)
    app.run (host="0.0.0.0", port=5000)

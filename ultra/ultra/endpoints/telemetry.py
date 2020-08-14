from flask_restful import Resource
from loguru import logger
from ultra.database import db
from ultra.models import Telemetry


class TelemetryEndpoint(Resource):
    """
    ``/telemetry` endpoint for handling forwarding of telemetry data
    """

    def get(self):
        # Get raw telemetry from DB
        try:
            telemetries = db.session.query(Telemetry) \
                                    .with_lockmode('read') \
                                    .all()
            return list(map(lambda x: x.to_json(), telemetries)), 200
        except Exception as e:
            logger.error(e)
            return {"message": "There was a problem fetching the telemetry. Please report this to the server admin with this message: {}".format(e)}, 500

from flask_restful import Resource
from loguru import logger
from ultra.database import db
from ultra.models import Telemetry


class TelemetryEndpoint(Resource):
    """
    /telemetry
    """

    def get(self):
        # Get raw telemetry from DB
        try:
            telemetries = db.session.query(Telemetry) \
                                    .with_lockmode('read') \
                                    .all()
            return list(map(lambda x: x.to_json(), telemetries))
        except Exception as e:
            logger.error(e)
            return "internal error fetching telemetry", 500

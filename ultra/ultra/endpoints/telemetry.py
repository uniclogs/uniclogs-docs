from flask_restful import Resource
from loguru import logger
import ultra
from ultra.database import db
from ultra.models import Telemetry, \
                         Items, \
                         ItemToDecomTableMappings


class TelemetryEndpoint(Resource):
    """
    /telemetry
    """

    def get(self):
        # Get raw telemetry from DB
        try:
            response = []
            telemetries = db.session.query(Telemetry) \
                                    .with_lockmode('read') \
                                    .all()
            telemetry_labels = db.session() \
                                 .query(Items.name, ItemToDecomTableMappings.item_index) \
                                 .with_lockmode('read') \
                                 .join(ItemToDecomTableMappings,
                                       Items.id == ItemToDecomTableMappings.id) \
                                 .filter(ItemToDecomTableMappings.packet_config_id == ultra.TELEMETRY_PACKET_CONFIG_ID) \
                                 .all()

            for telemetry in telemetries:
                tresponse = {}
                for label in telemetry_labels:
                    tresponse[label[0].lower()] = getattr(telemetry, 'i{}'.format(label[1]))
                response.append(tresponse)
            return response
        except Exception as e:
            logger.error(e)
            return "internal error fetching telemetry", 500

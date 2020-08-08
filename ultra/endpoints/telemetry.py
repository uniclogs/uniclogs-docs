from flask_restful import Resource
from database import db
from models import T2_0, \
                   Items, \
                   ItemToDecomTableMappings


class TelemetryEndpoint(Resource):
    """
    /telemetry
    """

    def get(self):
        # Get raw telemetry from DB
        # try:
        response = []
        telemetries = db.session.query(T2_0).with_lockmode('read').all()
        telemetry_labels = db.session() \
                             .query(Items.name, ItemToDecomTableMappings.item_index) \
                             .with_lockmode('read') \
                             .join(ItemToDecomTableMappings,
                                   Items.id == ItemToDecomTableMappings.id) \
                             .filter(ItemToDecomTableMappings.packet_config_id == 2) \
                             .all()

        print(telemetry_labels)
        for telemetry in telemetries:
            tresponse = {}
            for label in telemetry_labels:
                tresponse[label[0].lower()] = getattr(telemetry, 'i{}'.format(label[1]))
            response.append(tresponse)
        return response
        # except Exception:
        #     return "internal error fetching telemetry", 500

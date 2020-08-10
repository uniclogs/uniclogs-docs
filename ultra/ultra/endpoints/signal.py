from flask_restful import Resource


class SignalEndpoint(Resource):
    """
    Signal endpoint for ULTRA listends to signals from RADS and communicate all requests changed internally to CoSi
    """

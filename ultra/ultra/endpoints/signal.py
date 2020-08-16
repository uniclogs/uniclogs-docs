import ultra
from flask_restful import reqparse, Resource, inputs


class SignalEndpoint(Resource):
    """
    '/signal` endpoint for letting ULTRA know when a request was updated
    outside of ultra
    """

    def post(self):
        """
        Receives a signal that requests have been updated.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("token",
                            type=inputs.regex(ultra.ULTRA_TOKEN_PATTERN),
                            required=True,
                            location="headers")
        args = parser.parse_args()

        return {'message': 'Updates received, thanks for the tip pardner'}, 200

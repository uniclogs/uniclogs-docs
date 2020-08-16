import ultra
from flask import json
from flask_restful import reqparse, Resource, inputs
from loguru import logger
from ultra.database import db
from ultra.models import UserTokens, get_random_string


class UserTokenJsonEncoder(json.JSONEncoder):
    """
    JSON encoder for injecting python objects into JSON bodies of HTTP requests
    """

    def default(self, obj):
        if isinstance(obj, UserTokens):
            json_str = {
                    "token": obj.token,
                    "user_id": obj.user_id
                    }
            return json_str

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class UserEndpoint(Resource):
    """
    `/user` endpoint for handling creating a new user or forwarding existing
    user information
    """

    def get(self) -> [str, int]:
        """
        Gets the user associated with the token and all prevailing details

        Parameters
        ----------
        token: `str` Unique user token

        Returns
        -------
        `str`: The associated token details
        `int`: HTTP status code
        """

        parser = reqparse.RequestParser()
        parser.add_argument("token",
                            type=inputs.regex(ultra.ULTRA_TOKEN_PATTERN),
                            required=True,
                            location="headers")
        args = parser.parse_args()

        try:
            user = db.session.query(UserTokens) \
                        .with_lockmode('read') \
                        .filter(UserTokens.token == args["token"]) \
                        .first()
            return json.dumps(user, cls=UserTokenJsonEncoder), 201
        except Exception as e:
            logger.error(e)
            return {"Error": "There was a problem fetching the tokens. Please report this to the server admin with the message: {}".format(e)}, 500

    def post(self) -> [str, int]:
        """
        Makes a new request token for a user.

        Returns
        -------
        `str`: New UserToken data as a JSON or a error message.
        `int`: HTTP status code
        """

        parser = reqparse.RequestParser()
        parser.add_argument("username",
                            type=inputs.regex(ultra.ULTRA_USERNAME_PATTERN),
                            required=True,
                            location="json")
        args = parser.parse_args()

        try:
            new_token = get_random_string(128)
            new_user = UserTokens(token=new_token, user_id=args["username"])

            db.session.add(new_user)
            db.session.commit()

            return {"message": "Success: new user created",
                    "username": args["username"],
                    "token": new_token}, 201
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return {"message": "There was a problem with trying to create or submit a new user. Please contact the server admin with this message: {}".format(e)}, 500

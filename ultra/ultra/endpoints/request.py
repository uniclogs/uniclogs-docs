from flask_restful import reqparse, Resource, inputs
from loguru import logger
import ultra
from ultra.database import db
from ultra.models import Request, \
                         Pass, \
                         UserTokens

import pass_calculator as pc


class RequestEndpoint(Resource):
    """
    `/request` endpoint for handling a new request or fetching all requests
    """

    def get(self) -> [str, int]:
        """
        Get a list of all request given a user token

        Returns
        -------
        `str`: List of requests associated with a given user token
        `int`: HTTP status code
        """
        parser = reqparse.RequestParser()
        parser.add_argument("token",
                            type=inputs.regex(ultra.ULTRA_TOKEN_PATTERN),
                            required=True,
                            location="headers")
        args = parser.parse_args()
        user_request_list = []  # List of user request to return

        # Authenticate the incoming token
        try:
            token = db.session.query(UserTokens) \
                              .with_lockmode('read') \
                              .filter(UserTokens.token == args['token']) \
                              .first()
            if(token is None):
                return {'message': 'Invalid token'}, 401
        except Exception as e:
            return {'message': 'There was a problem trying to fetch the user tokens. Please report this to the server admin with this message: {}'.format(e)}

        try:
            result = db.session.query(Pass, Request) \
                               .with_lockmode('read') \
                               .join(Pass, Pass.uid == Request.pass_uid) \
                               .filter(Request.user_token == args['token']) \
                               .all()
        except Exception as e:
            return {"Error": "There was a problem fetching requests. Please report this to the server admin with this message: {}".format(e)}, 500

        # Make a nice list of dictionaries for easy conversion to JSON string
        for p, r in result:
            pass_data = pc.orbitalpass.OrbitalPass(
                    gs_latitude_deg=p.latitude,
                    gs_longitude_deg=p.longitude,
                    gs_elevation_m=p.elevation,
                    aos_utc=p.start_time,
                    los_utc=p.end_time,
                    horizon_deg=0.0
                    )

            user_request_list.append({"request_id": r.uid,
                                      "is_approved": r.is_approved,
                                      "is_sent": r.is_sent,
                                      "pass_data": pass_data,
                                      "created_date": r.created_date.isoformat(),
                                      "updated_date": r.updated_date.isoformat(),
                                      "observation_type": r.observation_type})
        return user_request_list, 200

    def post(self) -> [str, int]:
        """
        Make a new request associated with a given token

        Returns
        -------
        `str`: New request data as a JSON or a error message.
        `int`: HTTP Status code
        """

        parser = reqparse.RequestParser()
        parser.add_argument("token",
                            type=inputs.regex(ultra.ULTRA_TOKEN_PATTERN),
                            required=True,
                            location="headers")
        parser.add_argument("username",
                            default='',
                            location="headers")
        parser.add_argument("latitude",
                            required=True,
                            type=float,
                            location="json")
        parser.add_argument("longitude",
                            required=True,
                            type=float,
                            location="json")
        parser.add_argument("elevation_m",
                            default=0.0,
                            type=float)
        parser.add_argument("aos_utc",
                            required=True,
                            type=str,
                            location="json")
        parser.add_argument("los_utc",
                            required=True,
                            type=str,
                            location="json")
        args = parser.parse_args()

        # Authenticate the incoming token
        try:
            token_exists = db.session.query(UserTokens) \
                                     .with_lockmode('read') \
                                     .filter(UserTokens.token == args['token']) \
                                     .first() is not None
            if(not token_exists):
                return {'message': 'Invalid token'}, 401
        except Exception as e:
            return {'message': 'There was a problem trying to fetch the user tokens. Please report this to the server admin with this message: {}'.format(e)}, 500

        # Make datetime object from the HTTP args
        try:
            aos_utc = inputs.datetime_from_iso8601(args["aos_utc"])
            los_utc = inputs.datetime_from_iso8601(args["los_utc"])
        except Exception as e:
            logger.error("Invalid time-format for aos_utc/los_utc: {}"
                         .format(e))
            return {"Error": "Invalid time-format for aos_utc/los_utc"}, 401

        # TODO: Redo validation method with calculator

        # If needed, create the new pass in the DB
        new_pass = Pass(latitude=args["latitude"],
                        longitude=args["longitude"],
                        elevation=args["elevation_m"],
                        start_time=aos_utc,
                        end_time=los_utc)
        try:
            db_pass = db.session.query(Pass) \
                                .with_lockmode('read') \
                                .filter(Pass.latitude == args["latitude"],
                                        Pass.longitude == args["longitude"],
                                        Pass.start_time == aos_utc) \
                                .first()
            if(db_pass is None):
                db.session.add(new_pass)
                db.session.flush()

                new_pass = db.session.query(Pass) \
                                     .with_lockmode('read') \
                                     .filter(Pass.latitude == args["latitude"],
                                             Pass.longitude == args["longitude"],
                                             Pass.start_time == aos_utc) \
                                     .first()
            else:
                new_pass.uid = db_pass.uid
        except Exception as e:
            return {"message": "There was a problem trying to create or submit a new pass. Please report this to the server admin with this message: {}".format(e)}, 500

        # Create the new request and submit it to the DB
        try:
            new_request = Request(user_token=args['token'],
                                  is_approved=None,
                                  is_sent=False,
                                  pass_uid=new_pass.uid)

            db.session.add(new_request)
            db.session.commit()

            return {"message": "Success, request submitted",
                    "request_id": new_request.uid}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'There was a problem trying to create or submit a new request. Please report this to the server admin with this message: {}'.format(e)}, 500

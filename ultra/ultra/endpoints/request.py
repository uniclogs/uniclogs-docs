from flask_restful import reqparse, Resource, inputs
from sqlalchemy import func
from loguru import logger
import sys
from ultra.database import db
from ultra.models import Request, \
                         Tle, \
                         Pass, \
                         UserTokens, \
                         get_random_string
sys.path.insert(0, '..')
import pass_calculator as pc


class RequestEndpoint(Resource):
    """
    request endpoint for ULTRA to handle requesting oresat passes.
    """

    def post(self):
        # type: () -> str, int
        """
        Makes a new request for a user.

        Returns
        -------
        str
            New request data as a JSON or a error message.
        int
            error code
        """

        parser = reqparse.RequestParser()
        parser.add_argument("user_uid",
                            required=True,
                            type=inputs.regex('^\w{1,25}$'),
                            location="json")
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

        # TODO validate user token (Whenever user table is created)
        # TODO user check user day count (limit 10 req/day)

        # make datetime object from datetime str arg
        try:
            aos_utc = inputs.datetime_from_iso8601(args["aos_utc"])
            los_utc = inputs.datetime_from_iso8601(args["los_utc"])
        except Exception as e:
            logger.error(e)
            return {"Error": "Invalid format for aos_utc or los_utc."}, 401

        # validate pass
        try:
            latest_tle_time = db.session.query(func.max(Tle.time_added)) \
                                        .with_lockmode('read') \
                                        .one()
            latest_tle = db.session.query(Tle) \
                                   .with_lockmode('read') \
                                   .filter(Tle.time_added == latest_tle_time) \
                                   .one()
        except Exception:
            return {"Error": "internal TLE error"}, 400

        tle = [latest_tle.first_line, latest_tle.second_line]

        orbital_pass = pc.orbitalpass.OrbitalPass(
                gs_latitude_deg=args["latitude"],
                gs_longitude_deg=args["longitude"],
                aos_utc=aos_utc,
                los_utc=los_utc,
                gs_elevation_m=args["elevation_m"],
                horizon_deg=0.0
                )

        if not pc.calculator.validate_pass(tle, orbital_pass):
            return {"error": "Invalid pass"}, 401

        # make sure the pass is not already in db
        try:
            pass_check = db.session.query(Pass) \
                                   .with_lockmode('read') \
                                   .filter(Pass.latitude == args["latitude"],
                                           Pass.longitude == args["longitude"],
                                           Pass.start_time == aos_utc) \
                                   .all()
            if len(pass_check) != 0:
                return {"Error": "Pass already in db"}, 400
        except Exception:
            return {"Error": "internal TLE error"}, 400

        try:
            new_pass = Pass(
                    latitude=args["latitude"],
                    longitude=args["longitude"],
                    elevation=args["elevation_m"],
                    start_time=aos_utc,
                    end_time=los_utc
                    )

            db.session.add(new_pass)
            db.session.flush()

            user_token = get_random_string(4) + args["user_uid"] \
                                              + get_random_string(4)

            new_request = Request(
                    user_token=user_token,
                    is_approved=None,
                    is_sent=False,
                    pass_uid=new_pass.uid
            )

            db.session.add(new_request)
            db.session.flush()

            new_user_token = UserTokens(
                    token=new_request.user_token,
                    user_id=args["user_uid"]
            )

            db.session.add(new_user_token)
            db.session.flush()

            db.session.commit()

        except Exception:
            db.session.rollback()
        return {
                "message": "New request submitted.",
                "request_id": new_request.uid
                }

    def get(self):
        # type: () -> str, int
        """
        Get a list of all request for a user.

        Returns
        -------
        str
            List of request for a user or an error message as a JSON.
        int
            error code
        """

        user_request_list = []  # list of user request to return

        parser = reqparse.RequestParser()
        # user_uid length shouldn't be more than 25 chars
        parser.add_argument("user_uid",
                            type=inputs.regex('^\w{1,25}$'),
                            required=True,
                            location="json")
        args = parser.parse_args()

        # TODO user check user day count
        try:
            result = db.session.query(UserTokens, Pass) \
                            .join(Request,
                                  UserTokens.token == Request.user_token) \
                            .join(Pass, Pass.uid == Request.pass_uid) \
                            .filter(UserTokens.user_id == args["user_uid"]) \
                            .all()
        except Exception as e:
            logger.error(e)
            logger.error("Error fetching token '{}'".format(args["user_uid"]))
            return {"Error": "No requests or invalid user uid"}, 400

        # Make a nice list of dictionaries for easy conversion to JSON string
        for u, p in result:
            pass_data = pc.orbitalpass.OrbitalPass(
                    gs_latitude_deg=p.latitude,
                    gs_longitude_deg=p.longitude,
                    gs_elevation_m=p.elevation,
                    aos_utc=p.start_time,
                    los_utc=p.end_time,
                    horizon_deg=0.0
                    )

            user_request_list.append({"request_token": u.token,
                                      "pass_data": pass_data})

        return user_request_list

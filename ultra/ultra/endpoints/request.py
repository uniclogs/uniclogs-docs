from flask_restful import reqparse, Resource, inputs
from loguru import logger
import sys
import ultra
from ultra.database import db
from ultra.models import Request, \
                         Tle, \
                         Pass, \
                         UserTokens
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
        parser.add_argument("token",
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

        # TODO validate user token (Whenever user table is created)
        # TODO user check user day count (limit 10 req/day)

        # make datetime object from datetime str arg
        try:
            aos_utc = inputs.datetime_from_iso8601(args["aos_utc"])
            los_utc = inputs.datetime_from_iso8601(args["los_utc"])
        except Exception as e:
            logger.error(e)
            return {"Error": "Invalid time-format for aos_utc/los_utc."}, 401

        # Validate pass
        # try:
        #     latest_tle = db.session.query(Tle) \
        #                            .with_lockmode('read') \
        #                            .filter(Tle.first_line.contains(str(ultra.DEFAULT_NORAD_ID))) \
        #                            .order_by(Tle.time_added.desc()) \
        #                            .first()
        # except Exception:
        #     return {"Error": "There was an internal issue with grabing the latest TLE."}, 500

        # tle = [latest_tle.first_line, latest_tle.second_line]
        #
        # orbital_pass = pc.orbitalpass.OrbitalPass(
        #         gs_latitude_deg=args["latitude"],
        #         gs_longitude_deg=args["longitude"],
        #         aos_utc=aos_utc,
        #         los_utc=los_utc,
        #         gs_elevation_m=args["elevation_m"],
        #         horizon_deg=0.0
        #         )
        #
        # if not pc.calculator.validate_pass(tle, orbital_pass):
        #     return {"error": "Invalid pass"}, 422

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

        # try:
        new_pass = Pass(latitude=args["latitude"],
                        longitude=args["longitude"],
                        elevation=args["elevation_m"],
                        start_time=aos_utc,
                        end_time=los_utc)
        db.session.add(new_pass)
        db.session.flush()

        new_request = Request(
                user_token=args['token'],
                is_approved=None,
                is_sent=False,
                pass_uid=new_pass.uid
        )

        db.session.add(new_request)
        db.session.flush()

        db.session.commit()
        return {"message": "New request submitted.",
                "request_id": new_request.uid }, 201
        # except Exception:
        #     db.session.rollback()
        # finally:
        #     return {'message': 'Unhandled fatal error, please contact the server admin and report this.'}, 500

    def get(self):
        # type: () -> str, int
        """
        Get a list of all request for a user.FLICT (content): Merge conflict in ultra/ultra/endpoints/request.py

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
        parser.add_argument("token",
                            type=inputs.regex('^\w{1,25}$'),
                            required=True,
                            location="headers")
        args = parser.parse_args()

        # TODO user check user day count
        try:
            result = db.session.query(UserTokens, Pass) \
                               .join(Request,
                                     UserTokens.token == Request.user_token) \
                               .join(Pass, Pass.uid == Request.pass_uid) \
                               .filter(UserTokens.token == args["token"]) \
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

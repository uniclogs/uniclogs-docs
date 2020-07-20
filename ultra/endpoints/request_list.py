from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, inputs
from datetime import datetime, timezone, timedelta

import sys
sys.path.insert(0, '..')
import pass_calculator as pc


class RequestList(Resource):
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
        parser.add_argument("user_token", required=True, type=str, location="json")
        parser.add_argument("latitude", required=True, type=float, location="json")
        parser.add_argument("longitude", required=True, type=float, location="json")
        parser.add_argument("elevation_m", default=0.0, type=float)
        parser.add_argument("aos_utc", required=True, type=str, location="json")
        parser.add_argument("los_utc", required=True, type=str, location="json")
        args = parser.parse_args()

        # TODO validate user token
        # TODO user check user day count

        # make datetime object from datetime str arg
        try:
            aos_utc = inputs.datetime_from_iso8601(args["aos_utc"])
            los_utc = inputs.datetime_from_iso8601(args["los_utc"])
        except:
            return {"Error": "Invalid format for aos_utc or los_utc."}, 401

        tle = [ # TODO get from DB
                "1 25544U 98067A   20185.75040611  .00000600  00000-0  18779-4 0  9992",
                "2 25544  51.6453 266.4797 0002530 107.7809  36.4383 15.49478723234588"
                ]

        new_pass = pc.orbitalpass.OrbitalPass(
                gs_latitude_deg=args["latitude"],
                gs_longitude_deg=args["longitude"],
                gs_elevation_m=args["elevation_m"],
                aos_utc=aos_utc,
                los_utc=los_utc
                )

        if not pc.calculator.validate_pass(tle, new_pass):
            return {"error": "Invalid pass"}, 401

        """
        new_pass = Pass(
                latitude=args["latitude"],
                longtitude=args["longtitude"],
                elevation=args["elevation_m"],
                start_time=start_dt_utc,
                end_time=end_dt_utc
                )

        new_request = Request(
                user_token=args["user_token"],
                is_approved=False,
                is_sent=False,
                pass_uid=new_pass.uid,
                created_date=None # let model handle this
                )

        db.session.add(new_pass)
        db.session.add(new_request)
        db.session.commit()
        """

        return {"message": "New request submitted."}


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

        user_request_list = [] # list of user request to return

        parser = reqparse.RequestParser()
        parser.add_argument("user_token", required=True, type=str, location="json")
        args = parser.parse_args()

        # TODO validate user token
        # TODO user check user day count

        # get all request for user
        result = db.session.query(Request).join(Pass).filter(Request.user_token == args[user_token]).all()

        # make a nice list of dictionaries for easy conversion to JSON string
        for r in result:
            pass_data = pc.orbitalpass.OrbitalPass(
                    latitude = r.latitude,
                    longtitude= r.longtitude,
                    elevation_m =  r.elevation,
                    aos_utc = r.start_time,
                    los_utc = r.end_time,
                    horizon_deg = 0.0
                    )

            user_request_list.append({"request_id": r.uid, "pass_data": pass_data})

        return user_request_list

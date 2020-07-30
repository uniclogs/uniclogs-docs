from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, inputs
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from database import db
from models import Request, Tle, Pass, PassRequest

import sys
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

        # validate pass
        try:
            latest_tle_time = db.session.query(func.max(Tle.time_added)).one()
            latest_tle = db.session.query(Tle).filter(Tle.time_added == latest_tle_time).one()
        except:
            return {"Error" : "internal TLE error"}, 400

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
            pass_check = db.session.query(Pass).filter(
                    Pass.latitude == args["latitude"],
                    Pass.longtitude == args["longitude"],
                    Pass.start_time == aos_utc
                    ).all()
            if len(pass_check) != 0:
                return {"Error" : "Pass already in db"}, 400
        except:
            return {"Error" : "internal TLE error"}, 400

        new_pass = Pass(
                latitude = args["latitude"],
                longtitude = args["longitude"],
                elevation = args["elevation_m"],
                start_time = aos_utc,
                end_time = los_utc
                )

        db.session.add(new_pass)
        db.session.flush()

        new_request = Request(
                user_token = args["user_token"],
                is_approved = False,
                is_sent = False,
                pass_uid = new_pass.uid
                )

        db.session.add(new_request)
        db.session.flush()

        new_pass_request = PassRequest(
                pass_id = new_pass.uid,
                req_token = new_request.user_token
                )

        db.session.add(new_pass_request)
        db.session.flush()

        db.session.commit()

        return {
                "message": "New request submitted.",
                "request_id": new_request.pass_uid
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

        user_request_list = [] # list of user request to return

        parser = reqparse.RequestParser()
        parser.add_argument("user_token", required=True, type=str, location="json")
        args = parser.parse_args()

        # TODO validate user token
        # TODO user check user day count

        try:
            result = db.session.query(Pass)\
                           .join(Request, Pass.uid == Request.pass_uid)\
                           .all()
                           #.filter(Request.user_token == args["user_token"])\ TODO readd this when primary key is fixed
        except:
            return {"Error" : "No requests or invalid user token"}, 400

        # make a nice list of dictionaries for easy conversion to JSON string
        for r in result:
            pass_data = pc.orbitalpass.OrbitalPass(
                    gs_latitude_deg = r.latitude,
                    gs_longitude_deg = r.longtitude,
                    gs_elevation_m =  r.elevation,
                    aos_utc = r.start_time,
                    los_utc = r.end_time,
                    horizon_deg = 0.0
                    )

            user_request_list.append({"request_id": r.uid, "pass_data": pass_data})

        return user_request_list
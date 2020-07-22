from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, inputs
from datetime import datetime, timezone, timedelta
from database import db

import sys
sys.path.insert(0, "..")
import pass_calculator as pc


class Request(Resource):
    """
    request endpoint for ULTRA to handle requesting oresat passes.
    """

    def get(self, request_id):
        # type: () -> str, int
        """
        Get info request(s).

        request_id : int
            Request unique id.
        """
        print(request_id)

        parser = reqparse.RequestParser()
        parser.add_argument("user_token", required=True, type=str, location = "json")

        args = parser.parse_args()

        # TODO validate user token
        # TODO user check user day count

        # find request
        result = db.session.query(Request).join(Pass).filter(Pass.uid == request_id)
        if not result:
            return "Request not found", 400

        # make sure it owned by user
        if result.user_token == args["user_token"]:
            return "Permission denied. Request " + str(request_id) + \
                    " is not register to your token.", 400

        # convert dt obj to dt str
        start_dt_utc_str = result.start_time.replace(tzinfo=datetime.timezone.utc).isoformat()
        end_dt_utc_str = result.end_time.replace(tzinfo=datetime.timezone.utc).isoformat()

        # make a nice dictionary for easy conversion to JSON string
        request_entry = {
                "latitude": result.latitude,
                "longtitude": result.longtitude,
                "elevation_m": result.elevation,
                "aos_utc": start_dt_utc_str,
                "los_utc": end_dt_utc_str
                }

        return request_entry


    def put(self, request_id):
        # type: () -> str, int
        """
        Update request for a user.

        request_id : int
            Request unique id.
        """
        print(request_id)

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
        # TODO get latest TLE
        # TODO validate replacement pass

        # make sure request/pass exist in db
        result = db.session.query(Request).join(Pass).filter(Pass.uid == request_id)
        if not result:
            return "Request not found", 400

        # only can edit if is_approved is NULL
        if result.is_approved:
            return {"Error": "Can't use modied once approved for denied"}, 400

        # get pass
        pass_result = db.session.query(Pass).filter(Pass.uid == request_id)

        # make datetime object from datetime str arg
        try:
            start_dt_utc = inputs.datetime_from_iso8601(args["start_datetime_utc"])
            end_dt_utc = inputs.datetime_from_iso8601(args["end_datetime_utc"])
        except:
            return {"Error": "Invalid format for aos_utc or los_utc."}, 401

        # update entry
        pass_result = Pass(
                latitude=args["latitude"],
                longtitude=args["longtitude"],
                elevation=args["elevation_m"],
                start_time=start_dt_utc,
                end_time=end_dt_utc
                )

        db.session.commit()

        return {"message": "modified request succesful"}


    def delete(self, request_id):
        # type: () -> str, int
        """
        Delete request for a user.

        request_id : int
            Request unique id.
        """
        print(request_id)

        parser = reqparse.RequestParser()
        parser.add_argument("user_token", required=True, type=str, location="json")
        args = parser.parse_args()

        # TODO validate user token
        # TODO user check user day count
        # TODO delete from DB

        return {"message": "deleted request"}


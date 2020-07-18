"""
Request List Endpoint
=====================
For add a new request to a user request list or getting the list of request
for a user. Endpoint is /replace.

POST
----

Restful API endpoint for add a new request for a user.

Input:
    JSON str
        - user_token : user's token.
        - latitude : latitude degrees as a float.
        - longitude : longitude degrees as a float.
        - elevation_m : *Optional* elevation in meters as a float.
        - aos_utc : datetime as a string
        - los_utc : datetime as a string

    Example: ::

        {
            "token": 12345
            "name" : Bob
            "latitude": 45.512778,
            "longitude": 122.68278,
            "elevation_m": 0.0
            "aos_utc": "2020/07/13 14:24:25",
            "aos_utc": "2020/07/13 14:29:31",
        }

Output:
    A JSON message like
        {
            "message": "New request submitted. Request id: 12345"
        }

GET
---

Restful API endpoint for get a list of all request for a user.

Input:
    JSON str
        - user_token : user's token.

    Example: ::

        {
            "user_token": 12345
        }

Output:
    JSON str list of
        - request_id : the unique id for the request as a int,
        - latitude : latitude degrees as a float.
        - longitude : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - aos_utc : datetime string
        - stop_datetime_utc : datetime string

    Example: ::

        [
            {
                "request_id": 123,
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0
                "aos_utc": "2020/07/13 14:24:25",
                "stop_datetime_utc": "2020/07/13 14:29:42",
            },
            {
                "request_id": 134,
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0
                "aos_utc": "2020/07/13 16:01:42",
                "stop_datetime_utc": "2020/07/13 16:09:24",
            },
                "request_id": 141,
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0
                "aos_utc": "2020/07/13 19:15:55",
                "stop_datetime_utc": "2020/07/13 19:23:35",
            }
        ]

"""


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
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
        parser.add_argument("start_datetime_utc", required=True, type=str, location="json")
        parser.add_argument("end_datetime_utc", required=True, type=str, location="json")
        args = parser.parse_args()

        # TODO validate user token
        # TODO user check user day count

        # make datetime object from datetime str arg
        try:
            start_dt_utc = dateutil.parser.isoparse(args["start_datetime_utc"])
            end_dt_utc = dateutil.parser.isoparse(args["end_datetime_utc"])
        except:
            return {"Error": "Invalid format for aos_utc or los_utc."}, 401

        # TODO get latest TLE
        # TODO validate pass with pass calculator

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

        return "New request submitted. Request id:" + str(new_pass.uid), 201


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
            # convert dt obj to dt str
            aos_utc_str = r.start_time.replace(tzinfo=datetime.timezone.utc).isoformat()
            los_utc_str = r.end_time.replace(tzinfo=datetime.timezone.utc).isoformat()

            request_entry = {
                    "request_id": r.uid,
                    "latitude": r.latitude,
                    "longtitude": r.longtitude,
                    "elevation_m": r.elevation,
                    "aos_utc": aos_utc_str,
                    "los_utc": los_utc_str
                    }

            user_request_list.append(request_entry)

        return user_request_list, 200



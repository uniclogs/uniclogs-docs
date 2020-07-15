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
        - username : user's full name.
        - latitude_deg : latitude degrees as a float.
        - longitude_deg : longitude degrees as a float.
        - elevation_m : *Optional* elvation in meter as a float.
        - start_datetime_utc : datetime string

    Example: ::

        {
            "token": 12345
            "name" : Bob
            "latitude_deg": 45.512778,
            "longitude_deg": 122.68278,
            "elevation_m": 0.0
            "start_datetime_utc": "2020/07/13 14:24:25",
        }

Output:
    JSON str list of
        - request_id : the unique id for the request as a int,
        - latitude_deg : latitude degrees as a float.
        - longitude_deg : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - start_datetime_utc : datetime string
        - stop_datetime_utc : datetime string

    Example: ::

        {
            "request_id": 123,
            "latitude_deg": 45.512778,
            "longitude_deg": 122.68278,
            "elevation_m": 0.0
            "start_datetime_utc": "2020/07/13 14:24:25",
            "stop_datetime_utc": "2020/07/13 14:29:42",
        }

GET
---

Restful API endpoint for get a list of all request for a user.

Input:
    JSON str
        - user_token : user's token.
        - username : user's full name.

    Example: ::

        {
            "user_token": 12345
            "username" : Bob
        }

Output:
    JSON str list of
        - request_id : the unique id for the request as a int,
        - latitude_deg : latitude degrees as a float.
        - longitude_deg : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - start_datetime_utc : datetime string
        - stop_datetime_utc : datetime string

    Example: ::

        [
            {
                "request_id": 123,
                "latitude_deg": 45.512778,
                "longitude_deg": 122.68278,
                "elevation_m": 0.0
                "start_datetime_utc": "2020/07/13 14:24:25",
                "stop_datetime_utc": "2020/07/13 14:29:42",
            },
            {
                "request_id": 134,
                "latitude_deg": 45.512778,
                "longitude_deg": 122.68278,
                "elevation_m": 0.0
                "start_datetime_utc": "2020/07/13 16:01:42",
                "stop_datetime_utc": "2020/07/13 16:09:24",
            },
                "request_id": 141,
                "latitude_deg": 45.512778,
                "longitude_deg": 122.68278,
                "elevation_m": 0.0
                "start_datetime_utc": "2020/07/13 19:15:55",
                "stop_datetime_utc": "2020/07/13 19:23:35",
            }
        ]

"""


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime, timezone, timedelta

import sys
sys.path.insert(0, '..')
import pass_calculator.calculator as pc


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
        parser.add_argument("user_token", required=True, type=int, location="json")
        parser.add_argument("username", required=True, type=str, location="json")
        parser.add_argument("latitude_deg", required=True, type=float, location="json")
        parser.add_argument("longitude_deg", required=True, type=float, location="json")
        parser.add_argument("elevation_m", type=float)
        parser.add_argument("start_datetime_utc", required=True, type=str, location="json")
        args = parser.parse_args()

        print(args)
        return "new request", 201


    def get(self):
        # type: () -> str, int
        """
        Get a list of all request for a user.

        Returns
        -------
        str
            List of request for a user as a JSON.
        int
            error code
        """

        parser = reqparse.RequestParser()
        parser.add_argument("user_token", required=True, type=int, location="json")
        parser.add_argument("username", required=True, type=str, location="json")
        args = parser.parse_args()

        print(args)

        return "list", 201



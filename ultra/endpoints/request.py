"""
Request Endpoint
================
For reading, replacing, or deleting a specific request.
Endpoint is /replace/<int>.

GET
---

Get a info for a user's request.

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
        - latitude_deg : latitude degrees as a float.
        - longitude_deg : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - start_datetime_utc : datetime string
        - stop_datetime_utc : datetime string

    Example: ::

        {
            "latitude_deg": 45.512778,
            "longitude_deg": 122.68278,
            "elevation_m": 0.0
            "start_datetime_utc": "2020/07/13 14:24:25",
            "stop_datetime_utc": "2020/07/13 14:29:42",
        }

PUT
---

Replace the info for the user's request.

Input:
    JSON str
        - user_token : user's token.
        - username : user's full name.
        - latitude_deg : latitude degrees as a float.
        - longitude_deg : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - start_datetime_utc : datetime string

    Example: ::

        {
            "user_token": 12345
            "username" : Bob
            "latitude_deg": 45.512778,
            "longitude_deg": 122.68278,
            "elevation_m": 0.0
            "start_datetime_utc": "2020/07/13 14:24:25",
            "stop_datetime_utc": "2020/07/13 14:29:42",
        }

Output:
    JSON str list of
        - latitude_deg : latitude degrees as a float.
        - longitude_deg : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - start_datetime_utc : datetime string
        - stop_datetime_utc : datetime string

    Example: ::

        {
            "latitude_deg": 45.512778,
            "longitude_deg": 122.68278,
            "elevation_m": 0.0
            "start_datetime_utc": "2020/07/13 14:24:25",
            "stop_datetime_utc": "2020/07/13 14:29:42",
        }


DELETE
------

Delete the a user's request.

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
    JSON message
        - message : an error message or a success message

    Examples: ::

        {
            "message": "Request 12345 was deleted."
        }

        or

        {
            "message": "Permission denied."
        }

        or

        {
            "message": "Request 12345 was not found."
        }


"""


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime, timezone, timedelta

import sys
sys.path.insert(0, "..")
import pass_calculator.calculator as pc


class Request(Resource):
    """
"""


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime, timezone, timedelta

import sys
sys.path.insert(0, "..")
import pass_calculator.calculator as pc


class Request(Resource):
    """
    request endpoint for ULTRA to handle requesting oresat passes.
    """

    def get(self, request_id):
        # type: () -> str, int
        """
        Get info request(s).
        """
        print(request_id)

        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, type=int, location = "json")
        parser.add_argument("name", required=True, type=str, location = "json")

        args = parser.parse_args()

        print(args)

        return "request info", 201


    def put(self, request_id):
        # type: () -> str, int
        """
        Update request for a user.
        """
        print(request_id)

        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, type=int, location = "json")
        parser.add_argument("name", required=True, type=str, location = "json")
        parser.add_argument("latitude_deg", required=True, type=float, location="json")
        parser.add_argument("longitude_deg", required=True, type=float, location="json")
        parser.add_argument("elevation_m", type=float)
        parser.add_argument("start_datetime_utc", required=True, type=str, location="json")

        args = parser.parse_args()

        print(args)

        return "modified request", 201


    def delete(self, request_id):
        # type: () -> str, int
        """
        Delete request for a user.
        """
        print(request_id)

        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, type=int, location = "json")
        parser.add_argument("name", required=True, type=str, location = "json")

        print(args)

        args = parser.parse_args()

        return "deleted request", 201


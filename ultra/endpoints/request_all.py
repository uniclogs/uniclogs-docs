"""
Restful API endpoint for get a list of all request for a user.

Input:
    JSON str
        - token : user's token.
        - name : user's name.

    Example: ::

        {
            "token": 12345
            "name" : Bob
        }

Output:
    JSON str list of
        - start_datetime_utc : datetime string
        - duration_m : duration in mintues as a float

    Example: ::

        [
            {
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0
                "start_datetime_utc": "2020/07/13 14:24:25",
                "duration_m": 10.91405
            },
            {
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0
                "start_datetime_utc": "2020/07/13 16:01:42",
                "duration_m": 10.55885
            },
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0
                "start_datetime_utc": "2020/07/13 19:15:55",
                "duration_m": 10.88742
            }
        ]

"""


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime, timezone, timedelta

import sys
sys.path.insert(0, '..')
import pass_calculator.calculator as pc


class RequestAll(Resource):
    """
    request endpoint for ULTRA to handle requesting oresat passes.
    """

    def __init__(self):
        # get args
        self._parser = reqparse.RequestParser()
        super(AddRequest, self).__init__()

    def post(self):
        # type: () -> str, int
        """
        Makes a new request.
        """
        return "hi", 201


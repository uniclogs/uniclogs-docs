"""
Restful API endpoint for calculating orbital passes for locations.

Input:
    JSON str
        - latitude : latitude degrees as a float.
        - longitude : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.

    Example: ::

        {
            "latitude": 45.512778,
            "longitude": 122.68278,
            "elevation_m": 0.0
        }

Output:
    JSON str list of
        - start_datetime_utc : datetime string
        - duration_m : duration in mintues as a float

    Example: ::

        [
            {
                "start_datetime_utc": "2020/07/13 14:24:25",
                "duration_m": 10.91405
            },
            {
                "start_datetime_utc": "2020/07/13 16:01:42",
                "duration_m": 10.55885
            },
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


class Passes(Resource):
    """
    passes endpoint for ULTRA.
    """
    def __init__(self):
        # get args
        self._parser = reqparse.RequestParser()
        #self._parser.add_argument("latitude")
        self._parser.add_argument("latitude", required=True, type=float, location = "json")
        self._parser.add_argument("longitude", required=True, type=float, location = "json")
        self._parser.add_argument("elevation_m", type=float)
        super(Passes, self).__init__()

    def get(self):
        # type: () -> str, int
        """
        Calculautes orbital pass for API users.

        Returns
        -------
        str
            Orbital pass JSON str
        int
            error code

        """
        orbital_passes_dict = []
        #request.get_json(force=True)

        args = self._parser.parse_args()

        # get latest LTE and approved passes list from DB
        tle = [ # TODO get from DB
                "1 25544U 98067A   20185.75040611  .00000600  00000-0  18779-4 0  9992",
                "2 25544  51.6453 266.4797 0002530 107.7809  36.4383 15.49478723234588"
                ]
        approved_passes = [] # TODO get from DB

        # call pass calculator
        now = datetime.now()
        now = now.replace(tzinfo=timezone.utc)
        future = now + timedelta(days=7)
        future = future.replace(tzinfo=timezone.utc)
        orbital_passes = pc.get_all_passes(
                tle=tle,
                lat_deg=args["latitude"],
                long_deg=args["longitude"],
                start_time_utc=now,
                end_time_utc=future)

        # make list of dictionary from list of objects
        for op in orbital_passes:
            orbital_passes_dict.append(op)

        return orbital_passes_dict, 201


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime, timezone, timedelta

import sys
sys.path.insert(0, '..')
import pass_calculator.calculator as pc


class Passes(Resource):
    """
    /passes endpoint for ULTRA.
    """

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

        parser = reqparse.RequestParser()
        parser.add_argument("latitude", required=True, type=float, location = "json")
        parser.add_argument("longitude", required=True, type=float, location = "json")
        parser.add_argument("elevation_m", type=float)
        args = parser.parse_args()

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
                start_datetime_utc=now,
                end_datetime_utc=future
                )

        return orbital_passes, 200


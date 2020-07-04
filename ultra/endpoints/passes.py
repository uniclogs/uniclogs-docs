"""
passes
------

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
        - gs_latitude : ground station's latitude degrees as a float.
        - gs_longitude : ground station's longitude degrees as a float.
        - gs_elevation_m : ground station's elevation in meter as a float.
        - horizon_deg : horional degree as a float.
        - AOS_datetime_utc : datetime string
        - AOS_altitude : the altitude to the satellite at AOS as a float.
        - AOS_azimuth : the azimuth to the satellite at AOS as a float.
        - AOS_distance : the distance to satellite at AOS as a float.
        - LOS_datetime_utc : datetime string

    Example: ::

        [
            {
                "gs_latitude": 45.512778,
                "gs_longitude": 122.68278,
                "gs_elevation_m": 0.0,
                "horizon_deg": 0.0,
                "AOS_datetime_utc": "2020/07/13 14:24:25",
                "AOS_altitude": 4.864712542119566e-06,
                "AOS_azimuth": 241.68340903163806,
                "AOS_distance": 2354.627989427095,
                "LOS_datetime_utc": "2020/07/13 14:35:20"
            },
            {
                "gs_latitude": 45.512778,
                "gs_longitude": 122.68278,
                "gs_elevation_m": 0.0,
                "horizon_deg": 0.0,
                "AOS_datetime_utc": "2020/07/13 16:01:42",
                "AOS_altitude": 0.006386112928720387,
                "AOS_azimuth": 275.644343752701,
                "AOS_distance": 2360.087702168765,
                "LOS_datetime_utc": "2020/07/13 16:12:15"
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

        # get args
        parser = reqparse.RequestParser()
        parser.add_argument("latitude", required=True, type=float)
        parser.add_argument("longitude", required=True, type=float)
        parser.add_argument("elevation_m", type=float)
        args = parser.parse_args()

        print(args)

        # get latest LTE and approved passes list from DB
        tle =[ # TODO get from DB
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
            orbital_passes_dict.append(op.__dict__)

        return orbital_passes_dict, 201


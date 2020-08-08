from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from database import db
from models import Tle

import sys
sys.path.insert(0, '..')
import pass_calculator.calculator as pc


class PassesEndpoint(Resource):
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

        # get latest LTE from DB
        try:
            latest_tle_time = db.session.query(func.max(Tle.time_added)).one()
            latest_tle = db.session.query(Tle).filter(Tle.time_added == latest_tle_time).one()
        except:
            return "internal TLE error", 400
        tle = [
                latest_tle.first_line,
                latest_tle.second_line
                ]

        # get latest LTE and approved passes list from DB
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
                end_datetime_utc=future,
                approved_passes=approved_passes
                )

        return orbital_passes, 200

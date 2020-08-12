from flask_restful import reqparse, Resource
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from ultra.database import db
from ultra.models import Tle
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
        parser = reqparse.RequestParser()
        parser.add_argument("latitude",
                            required=True,
                            type=float,
                            location="args")
        parser.add_argument("longitude",
                            required=True,
                            type=float,
                            location="args")
        parser.add_argument("elevation_m", type=float)
        args = parser.parse_args()

        # Get latest TLE from DB
        try:
            latest_tle_time = db.session.query(func.max(Tle.time_added)).one()
            latest_tle = db.session.query(Tle).filter(Tle.time_added == latest_tle_time).one()
        except Exception:
            return "internal TLE error", 400
        tle = [
                latest_tle.first_line,
                latest_tle.second_line
                ]

        # Get latest TLE and approved passes list from the DB
        approved_passes = []  # TODO get from DB

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

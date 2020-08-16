import ultra.models as models
import pass_calculator.calculator as pc
from flask_restful import reqparse, Resource
from datetime import datetime, timezone, timedelta
from ultra.database import db


class PassesEndpoint(Resource):
    """
    `/passes` endpoint for getting available passes for OreSat and a
    coinciding location
    """

    def get(self) -> [str, int]:
        """
        Calculautes orbital pass for API users.

        Returns
        -------
        `str`: Orbital pass data
        `int`: HTTP Status code
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
            latest_tle = db.session.query(models.Tle) \
                                   .with_lockmode('read') \
                                   .order_by(models.Tle.time_added.desc()) \
                                   .first()
        except Exception as e:
            return {'message': 'There was a problem fetching the latests TLEs. Please report this to the server admin with this message: {}'.format(e)}, 500
        tle = [latest_tle.first_line, latest_tle.second_line]

        # Get already approved passes list from the DB and remove them
        #   from the calculated orbital passes
        approved_passes = db.session.query(models.Pass) \
                                    .with_lockmode('read') \
                                    .join(models.Request,
                                          models.Pass.uid == models.Request.pass_uid) \
                                    .filter(models.Request.is_approved) \
                                    .all()
        # Convert the list of Pass objects to OrbitalPass objects
        approved_passes = list(map(lambda x: x.to_orbital_pass(), approved_passes))

        # Call pass calculator
        now = datetime.now()
        now = now.replace(tzinfo=timezone.utc)
        future = now + timedelta(days=7)
        future = future.replace(tzinfo=timezone.utc)
        orbital_passes = pc.get_all_passes(tle=tle,
                                           lat_deg=args["latitude"],
                                           long_deg=args["longitude"],
                                           start_datetime_utc=now,
                                           end_datetime_utc=future,
                                           approved_passes=approved_passes)
        return orbital_passes, 200

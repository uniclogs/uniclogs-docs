import sys
import ballcosmos.script as bcs
from flask_restful import reqparse, \
                          Resource, \
                          inputs
from sqlalchemy import func
from loguru import logger
from ultra.database import db
from ultra.models import Request, \
                         Tle, \
                         Pass
sys.path.insert(0, "..")
import pass_calculator as pc


class RequestIdEndpoint(Resource):
    """
    request endpoint for ULTRA to handle requesting oresat passes.
    """

    def get(self, request_id: int) -> [str, int]:
        """
        Get info request(s).

        request_id: `int` Request unique id.
        """
        try:
            result = db.session.query(Pass) \
                           .with_lockmode('read') \
                           .join(Request, Pass.uid == Request.pass_uid) \
                           .filter(Request.uid == request_id) \
                           .one()
        except Exception as e:
            logger.error(e)
            logger.error("Error fetching req id '{}'".format(request_id))
            return {"Error": "No matching pass or wrong user token"}, 400

        pass_data = pc.orbitalpass.OrbitalPass(
                gs_latitude_deg=result.latitude,
                gs_longitude_deg=result.longitude,
                gs_elevation_m=result.elevation,
                aos_utc=result.start_time,
                los_utc=result.end_time,
                horizon_deg=0.0
                )

        return pass_data

    def put(self, request_id: int) -> [str, int]:
        """
        Update request for a user.

        request_id: `int` Request unique id.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("latitude",
                            required=True,
                            type=float,
                            location="json")
        parser.add_argument("longitude",
                            required=True,
                            type=float,
                            location="json")
        parser.add_argument("elevation_m",
                            default=0.0,
                            type=float)
        parser.add_argument("aos_utc",
                            required=True,
                            type=str,
                            location="json")
        parser.add_argument("los_utc",
                            required=True,
                            type=str,
                            location="json")

        args = parser.parse_args()

        request = None
        try:
            request = db.session.query(Request) \
                                .with_lockmode('read') \
                                .filter(Request.uid == request_id) \
                                .one()
        except Exception as e:
            logger.error(e)
            return {"Error": "No matching pass or wrong user token"}, 400

        if request is None or request.is_approved:
            return {"Error": "Request doesn't exist or is already approved"}, \
                   400

        try:
            result = db.session.query(Pass) \
                               .with_lockmode('update') \
                               .filter(Pass.uid == request.pass_uid) \
                               .one()
        except Exception as e:
            logger.error(e)
            return {"Error": "No matching pass or wrong assigned pass_uid"}, 400

        try:
            latest_tle_time = db.session.query(func.max(Tle.time_added)) \
                                        .with_lockmode('read') \
                                        .one()
            latest_tle = db.session.query(Tle) \
                                   .with_lockmode('read') \
                                   .filter(Tle.time_added == latest_tle_time) \
                                   .one()
        except Exception as e:
            logger.error(e)
            return {"Error": "internal TLE error"}, 400

        tle = [latest_tle.first_line, latest_tle.second_line]

        # make orbital pass object
        try:
            aos_utc = inputs.datetime_from_iso8601(args["aos_utc"])
            los_utc = inputs.datetime_from_iso8601(args["los_utc"])
        except Exception as e:
            logger.error(e)
            return {"Error": "Invalid format for aos_utc or los_utc."}, 401

        input_orbital_pass = pc.orbitalpass.OrbitalPass(
                gs_latitude_deg=args["latitude"],
                gs_longitude_deg=args["longitude"],
                aos_utc=aos_utc,
                los_utc=los_utc,
                gs_elevation_m=args["elevation_m"],
                horizon_deg=0.0
                )

        # validate replacement pass
        if not pc.calculator.validate_pass(tle=tle,
                                           orbital_pass=input_orbital_pass):
            return {"Error": "Invalid pass."}, 401

        # TODO check to see if other requested the same pass, if they have,
        # then make an new Pass for this user

        # update entry
        result.latitude = input_orbital_pass.gs_latitude_deg,
        result.longitude = input_orbital_pass.gs_longitude_deg,
        result.elevation = input_orbital_pass.gs_elevation_m,
        result.horizon_deg = input_orbital_pass.horizon_deg,
        result.start_time = input_orbital_pass.aos_utc,
        result.end_time = input_orbital_pass.los_utc

        db.session.commit()

        return {"message": "Request {} succesfully modified."
                .format(request_id)}

    def delete(self, request_id: int) -> [str, int]:
        """
        Delete request for a user.

        request_id: `int` Request unique id.
        """

        try:
            request_result = db.session.query(Request) \
                                       .with_lockmode('update') \
                                       .filter(Request.uid == request_id) \
                                       .one()

            if request_result.is_approved and request_result.is_sent:
                bcs.cmd('ENGR_LINK PASS_CANCEL with TYPE NORMAL, PASS_ID {}'
                        .format(request_id))
            else:
                request_result.is_approved = False

            db.session.commit()

        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return {"Error": "No matching pass or wrong user token"}, 400

        return {"message": "Deleted request {}".format(request_id)}

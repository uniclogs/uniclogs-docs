import ultra
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
import pass_calculator as pc


class RequestIdEndpoint(Resource):
    """
    `/request` endpoint for handling request-specific actions like updating a
    time-and-place, or canceling a previously scheduled pass
    """

    def get(self, request_id: int) -> [str, int]:
        """
        Get a singular request by id
        request_id: `int` Request id

        Returns:
        --------
        `int`: HTTP Status code
        """
        parser = reqparse.RequestParser()
        parser.add_argument("token",
                            type=inputs.regex(ultra.ULTRA_TOKEN_PATTERN),
                            required=True,
                            location="headers")
        args = parser.parse_args()

        try:
            pass_request = db.session.query(Pass, Request) \
                                     .with_lockmode('read') \
                                     .join(Request, Pass.uid == Request.pass_uid) \
                                     .filter(Request.uid == request_id) \
                                     .one()
        except Exception as e:
            logger.error(e)
            logger.error("Error fetching req id '{}'".format(request_id))
            return {"Error": "No request matching id: {}"
                    .format(request_id)}, 400

        pass_data = pc.orbitalpass.OrbitalPass(
                        gs_latitude_deg=pass_request.latitude,
                        gs_longitude_deg=pass_request.longitude,
                        gs_elevation_m=pass_request.elevation,
                        aos_utc=pass_request.start_time,
                        los_utc=pass_request.end_time,
                        horizon_deg=0.0)

        if(pass_data.token == args['token']):
            return pass_data, 200
        else:
            return {'message': 'Unauthorized: the token: {} does not own the \
                     request with id: {}'.format(args['token'], request_id)}, \
                     403

    def put(self, request_id: int) -> [str, int]:
        """
        Update as singular request for a user

        request_id: `int` Request unique id.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("token",
                            type=inputs.regex(ultra.ULTRA_TOKEN_PATTERN),
                            required=True,
                            location="headers")
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

        # TODO: Review this
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

        return {"message": "Succes: request modified".format(request_id),
                "user": result}, 201

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

            if(request_result is None):
                return {"Error": "No request with matching id",
                        "request_id": request_id}, 404

            if request_result.is_approved and request_result.is_sent:
                bcs.cmd('ENGR_LINK PASS_CANCEL with TYPE NORMAL, PASS_ID {}'
                        .format(request_id))
            else:
                request_result.is_approved = False
            db.session.commit()

            return {"message": "Succes: canceled request".format(request_id),
                    "request": request_result}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return {"message": "There was a problem trying to delete the request. Please report this to the server admin with this message: {}".format(e)}, 500

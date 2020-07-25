from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, inputs
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from database import db
from models import Request, Tle, Pass, PassRequest, testTleModel
from loguru import logger

import sys
sys.path.insert(0, "..")
import pass_calculator as pc


class RequestIdEndpoint(Resource):
    """
    request endpoint for ULTRA to handle requesting oresat passes.
    """

    def get(self, request_id):
        # type: () -> str, int
        """
        Get info request(s).

        request_id : int
            Request unique id.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("user_token", required=True, type=str, location = "json")

        args = parser.parse_args()

        # TODO user check user day count
        testTleModel()
        try:
            print("test)")
            result = db.session.query(Pass)\
                           .join(Request, Pass.uid == Request.pass_uid)\
                           .filter(Pass.uid == request_id and Request.user_token == args["user_token"])\
                           .one()
            print(result)
        except Exception as e:
            logger.error(e)
            logger.error("Error fetching token '{}'".format(args["user_token"]))
            return {"Error" : "No matching pass or wrong user token"}, 400


        pass_data = pc.orbitalpass.OrbitalPass(
                gs_latitude_deg = result.latitude,
                gs_longitude_deg = result.longtitude,
                gs_elevation_m =  result.elevation,
                aos_utc = result.start_time,
                los_utc = result.end_time,
                horizon_deg = 0.0
                )

        return pass_data


    def put(self, request_id):
        # type: () -> str, int
        """
        Update request for a user.

        request_id : int
            Request unique id.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("user_token", required=True, type=str, location="json")
        parser.add_argument("latitude", required=True, type=float, location="json")
        parser.add_argument("longitude", required=True, type=float, location="json")
        parser.add_argument("elevation_m", default=0.0, type=float)
        parser.add_argument("aos_utc", required=True, type=str, location="json")
        parser.add_argument("los_utc", required=True, type=str, location="json")

        args = parser.parse_args()

        # TODO user check user day count

        try:
            result = db.session.query(Pass)\
                   .join(Request, Pass.uid == Request.pass_uid)\
                   .filter(Pass.uid == request_id and
                           Request.user_token == args["user_token"])\
                   .one()
        except DbException:
            return {"Error" : "No matching pass or wrong user token"}, 400

        try:
            latest_tle_time = db.session.query(func.max(Tle.time_added)).one()
            latest_tle = db.session.query(Tle).filter(Tle.time_added == latest_tle_time).one()
        except:
            return {"Error" : "internal TLE error"}, 400

        tle = [latest_tle.first_line, latest_tle.second_line]

        # make orbital pass object
        try:
            aos_utc = inputs.datetime_from_iso8601(args["aos_utc"])
            los_utc = inputs.datetime_from_iso8601(args["los_utc"])
        except:
            return {"Error": "Invalid format for aos_utc or los_utc."}, 401

        input_orbital_pass = pc.orbitalpass.OrbitalPass(
                gs_latitude_deg = args["latitude"],
                gs_longitude_deg = args["longitude"],
                aos_utc = aos_utc,
                los_utc = los_utc,
                gs_elevation_m = args["elevation_m"],
                horizon_deg = 0.0
                )

        # validate replacement pass
        if not pc.calculator.validate_pass(tle=tle, orbital_pass=input_orbital_pass):
            return {"Error": "Invalid pass."}, 401

        #TODO check to see if other requested the same pass, if theya have make an new Pass for this user

        # update entry
        result.latitude = input_orbital_pass.gs_latitude_deg,
        result.longtitude = input_orbital_pass.gs_longitude_deg,
        result.elevation = input_orbital_pass.gs_elevation_m,
        result.horizon_deg = input_orbital_pass.horizon_deg,
        result.start_time = input_orbital_pass.aos_utc,
        result.end_time = input_orbital_pass.los_utc

        db.session.commit()

        return {"message": "Request {} succesfully modified.".format(request_id)}


    def delete(self, request_id):
        # type: () -> str, int
        """
        Delete request for a user.

        request_id : int
            Request unique id.
        """

        parser = reqparse.RequestParser()
        parser.add_argument("user_token", required=True, type=str, location="json")
        args = parser.parse_args()

        # TODO user check user day count

        try:
            pass_result = db.session.query(Pass)\
                    .filter(Pass.uid == request_id)\
                    .one()
            request_result = db.session.query(Request)\
                   .filter(Request.pass_uid == request_id and
                           Request.user_token == args["user_token"])\
                   .one()
            pass_request_result = db.session.query(PassRequest)\
                   .filter(PassRequest.pass_id == request_id and
                           PassRequest.req_token == args["user_token"])\
                   .one()
        except:
            return {"Error" : "No matching pass or wrong user token"}, 400

        db.session.delete(pass_request_result) # NOTE or should flip a flag?
        db.session.flush()
        db.session.delete(request_result) # NOTE or should flip a flag?
        db.session.flush()
        db.session.delete(pass_result) # NOTE or should flip a flag?
        db.session.flush()
        db.session.commit()

        return {"message": "Deleted request {}".format(request_id)}

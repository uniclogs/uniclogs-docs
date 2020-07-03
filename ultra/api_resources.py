from api_json_definitions import *
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


class Passes(Resource):
    def put(self):
        # get args
        parser = reqparse.RequestParser()
        parser.add_argument("calc_data")
        args = parser.parse_args()

        pass_calc_data = args["calc_data"]

        #TODO replace with call to pass calcualtor
        from datetime import datetime
        now = datetime.utcnow()
        date_time = now.strftime("%Y/%m/%d, %H:%M:%S")
        temp_pass = PassDef
        temp_pass["start_datetime_utc"] = date_time
        temp_pass["end_datetime_utc"] = date_time
        possible_passes = {"possible_pass_list": [
            temp_pass,
            temp_pass,
            temp_pass,
            temp_pass,
            ]
        }

        return possible_passes, 201


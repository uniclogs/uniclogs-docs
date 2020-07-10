from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime, timezone, timedelta

import sys
sys.path.insert(0, "..")
import pass_calculator.calculator as pc


class Request(Resource):
    """
    request endpoint for ULTRA to handle requesting oresat passes.
    """

    def __init__(self):
        # get args
        self._parser = reqparse.RequestParser()
        super(ModifyRequest, self).__init__()


    def get(self, request_id):
        # type: () -> str, int
        """
        Get info request(s).
        """
        print(request_id)

        return "hi", 201


    def put(self, request_id):
        # type: () -> str, int
        """
        Update request for a user.
        """
        print(request_id)

        return "hi", 201


    def delete(self, request_id):
        # type: () -> str, int
        """
        Delete request for a user.
        """
        print(request_id)

        return "hi", 201


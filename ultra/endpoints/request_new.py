from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime, timezone, timedelta

import sys
sys.path.insert(0, '..')
import pass_calculator.calculator as pc


class RequestNew(Resource):
    """
    request endpoint for ULTRA to handle requesting oresat passes.
    """

    def __init__(self):
        # get args
        self._parser = reqparse.RequestParser()
        super(AddRequest, self).__init__()

    def post(self):
        # type: () -> str, int
        """
        Makes a new request.
        """
        return "hi", 201


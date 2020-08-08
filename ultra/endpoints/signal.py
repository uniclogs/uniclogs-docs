from flask import Flask, json
from flask_restful import reqparse, abort, Api, Resource, inputs
from database import db
from models import UserTokens
from loguru import logger

import sys
sys.path.insert(0, "..")


class SignalEndpoint(Resource):
    """
    Signal endpoint for ULTRA listends to signals from RADS and communicate all requests changed internally to CoSi
    """

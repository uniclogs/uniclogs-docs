from .satnogs import *
from .spacetrack import *
from .pass_calculator import *
from .dart_db import DartDB
from .common import DB_HOST, \
                    DB_PROD_PATH, \
                    DB_USERNAME, \
                    DB_PASSWORD

DATABASE = DartDB(DB_HOST, DB_PROD_PATH, DB_USERNAME, DB_PASSWORD)


def get_all_requests():
    return []


def get_active_requests():
    return []


def get_archived_requests():
    return []

# connect to the Space-Track.org API
# spaceTrack.py
# need space-track.org un/pw credentials and norad_id for satellite

import sys
import requests
import json
from .common import *

sys.path.append('..')
from database import DartDB

DATABASE = DartDB(DB_HOST, DB_PROD_PATH, DB_USERNAME, DB_PASSWORD)


class TLERequestFailed(Exception):
    def __init___(self, args):
        super().__init__(self, "Exception raised with arguments {0}".format(args))
        self.args = args


def get_tle(user, password, norad_id):
    credentials = {'identity': user, 'password': password}
    data = []
    sat_id = norad_id

    with requests.Session() as session:
        resp = session.post(URL_BASE + REQUEST_LOGIN, data=credentials)
        if resp.status_code != 200:
            raise TLERequestFailed(resp, "Credentials fail on login")

        resp = session.get(URL_BASE + TLE_URI + str(sat_id) + REQUEST_DETAILS)
        if resp.status_code != 200:
            print(resp)
            raise TLERequestFailed(resp, "TLE request fails, check credentials")

        # output to file in json format
        data = json.loads(resp.text)

    # Return data from function
    return data

# if __name__ == "__main__":
#     siteCred = credentials(usr, pwd)
#     tleOutput = getTLE(siteCred, norad_id)

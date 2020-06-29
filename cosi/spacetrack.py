import requests
import json
from .common import SPACETRACK_LOGIN, \
                    SPACETRACK_USERNAME, \
                    SPACETRACK_PASSWORD, \
                    SPACETRACK_TLE, \
                    EnvironmentVariableNotDefined

# connect to the Space-Track.org API
# spaceTrack.py
# need space-track.org un/pw credentials and norad_id for satellite


class TLERequestFailed(Exception):
    def __init___(self, reason: str, response: dict):
        super().__init__(self, "TLE request failure: " + reason
                         + '\n\tResponse Body: ' + str(response))
        self.response = response


def request_tle(norad_id):
    if(SPACETRACK_USERNAME is None):
        raise EnvironmentVariableNotDefined("SPACETRACK_USERNAME")
    if(SPACETRACK_PASSWORD is None):
        raise EnvironmentVariableNotDefined("SPACETRACK_PASSWORD")

    credentials = {'identity': SPACETRACK_USERNAME,
                   'password': SPACETRACK_PASSWORD}
    data = []

    with requests.Session() as session:
        res = session.post(SPACETRACK_LOGIN, data=credentials)
        if res.status_code != 200:
            raise TLERequestFailed("Bad credentials!", res)

        res = session.get(SPACETRACK_TLE.replace('NID', str(norad_id)))
        if res.status_code != 200:
            raise TLERequestFailed("Bad request!", res)
        data = json.loads(res.text)
    return data

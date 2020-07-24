import requests
import json
from .common import SPACETRACK_LOGIN, \
                    SPACETRACK_USERNAME, \
                    SPACETRACK_PASSWORD, \
                    SPACETRACK_TLE, \
                    EnvironmentVariableNotDefined


class TLERequestFailed(Exception):
    """An error specification.
    This is thrown when a satellite is retrieved from Satnogs, but the decoder
    for it is unknown/unavailable, hence making it imposible to decode the
    telemetry frame.

    Attributes
    ---------
    args : Error details
        In-length details about what broke.
    """

    def __init___(self, reason: str, response: dict):
        super().__init__(self, "TLE request failure: " + reason
                         + '\n\tResponse Body: ' + str(response))
        self.response = response


def request_tle(norad_id):
    """Makes a request to space-track.org for the latest TLE of a satellite specified by Norad ID.

    Parameters
    ----------
    norad_id : Satellite Norad ID
        A unique satellite identifier.

    Returns
    -------
    list :
        dict :
            -- TLE_LINE0 : TLE header
            -- TLE_LINE1 : TLE first line or entry
            -- TLE_LINE2 : TLE second line or entry
    """
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

        res = session.get(SPACETRACK_TLE.format(norad_id))
        if res.status_code != 200:
            raise TLERequestFailed("Bad request!", res)
        data = json.loads(res.text)[0]
    return data

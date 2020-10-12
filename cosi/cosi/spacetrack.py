import requests
import json
import cosi


class TLERequestFailed(Exception):
    """An error specification.
    This is thrown when a satellite is retrieved from Satnogs, but the decoder
    for it is unknown/unavailable, hence making it imposible to decode the
    telemetry frame.

    Attributes
    ---------
    reason: `str` In-length details about what broke.
    response: `dict` The HTTP response body from spacetrack
    """

    def __init___(self, reason: str, response: dict):
        super().__init__(self, "TLE request failure: " + reason
                         + '\n\tResponse Body: ' + str(response))
        self.response = response


def request_tle(norad_id: int) -> dict:
    """Makes a request to space-track.org for the latest TLE of a satellite
    specified by Norad ID.

    Parameters
    ----------
    norad_id: `int` A unique satellite identifier

    Returns
    -------
    dict:
    * "TLE_LINE0": `str` TLE header
    * "TLE_LINE1": `str` TLE first line or entry
    * "TLE_LINE2": `str` TLE second line or entry

    Raises
    ------
    `EnvironmentError`: Raises this if one or more of of the following
    environment variables are not defined
    * `SPACETRACK_USERNAME`
    * `SPACETRACK_PASSWORD`

    `TLERequestFailed`: Raises this if any non-200 resonse was recieved
    from spacetrack
    * Bad credentials
    * Bad request header
    * No TLEs found for requested satellite
    """
    if(cosi.SPACETRACK_USERNAME is None):
        raise EnvironmentError("Enviromnemt Variable {} is not defined!"
                               .format('SPACETRACK_USERNAME'))
    if(cosi.SPACETRACK_PASSWORD is None):
        raise EnvironmentError("Enviromnemt Variable {} is not defined!"
                               .format('SPACETRACK_PASSWORD'))

    credentials = {'identity': cosi.SPACETRACK_USERNAME,
                   'password': cosi.SPACETRACK_PASSWORD}
    data = []

    with requests.Session() as session:
        res = session.post(cosi.SPACETRACK_LOGIN, data=credentials)
        if res.status_code != 200:
            raise TLERequestFailed("Bad credentials!", res)

        res = session.get(cosi.SPACETRACK_TLE.format(norad_id))
        if res.status_code != 200:
            raise TLERequestFailed("Bad request!", res)
        data = json.loads(res.text)
        if(len(data) > 0):
            data = data[0]
        else:
            raise TLERequestFailed('No TLEs found for satellite: ({}: {})'
                                   .format(norad_id, data))
    return data

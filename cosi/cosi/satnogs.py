import requests
import datetime
import cosi
import cosi.structs.csim as csim
from pytz import utc


class NoDecoderForTelemetryFrame(Exception):
    """An error specification.
    This is thrown when a satellite is retrieved from Satnogs, but the decoder
    for it is unknown/unavailable, hence making it imposible to decode the
    telemetry frame.

    Attributes
    ---------
    args: `[str]` In-length details about what broke.
    """

    def __init__(self, args):
        super().__init__(self, "Decoder frame failure! \
                                Failed with arguments: " + str(args))
        self.args = args


def get_age(first: datetime.datetime,
            second: datetime.datetime = datetime.datetime.now(utc)) \
            -> datetime.timedelta:
    """Gets the time difference or "age" between two different times.

    Parameters
    ----------
    first: `datetime.datetime` The first date-time
    second: `datetime.datetime` The second date-time

    Returns
    -------
    `datetime.timedelta`: The time difference
    """
    return second - first


def request_satellite(norad_id: int = None) -> dict:
    """Makes a request to satnogs for metadata on the satellite specified by
    Norad ID

    Parameters
    ----------
    norad_id: `int` A unique satellite identifier

    Returns
    -------
    `dict`: A python dictionary containing useful metadata about the satellite

    Raises
    ------
    `socket.gaierror`: Raises this when there's an error with\
    the HTTP request to satnogs
    """
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}
    parameters = {'format': 'json', 'norad_cat_id': str(norad_id)}
    return requests.get(cosi.SATNOGS_SATELITE.format(norad_id),
                        headers=headers,
                        params=parameters,
                        allow_redirects=True).json()


def request_telemetry(norad_id: int = None) -> dict:
    """Makes a request to satnogs.org for the raw telemetry frame of the
    satellite specified by Norad ID

    Parameters
    ----------
    norad_id: `int` A unique satellite identifier

    Returns
    -------
    dict:
    * norad_cat_id: `int` A unique satellite identifier
    * transmitter: `str` ? (optional)
    * app_source: `str` ?
    * schema: `str` api schema (optional)
    * decoded: `str` ? (optional)
    * frame: `byte` The raw and encoded telemetry frame
    * timestamp: `int` Timestamp of when the frame was constructed

    Raises
    ------
    `ValueError`: Raises this when telemetry frames are not supported for the
    satellite specified
    `socket.gaierror`: Raises this when there's an error with\
    the HTTP request to satnogs
    """
    if(cosi.SATNOGS_TOKEN is None):
        raise ValueError("Enviromnemt Variable {} is not defined!"
                         .format('SATNOGS_TOKEN'))

    headers = {'Authorization': "Token " + cosi.SATNOGS_TOKEN,
               'Content-Type': 'application/json'}
    parameters = {'format': 'json', 'norad_cat_id': str(norad_id)}
    response = requests.get(cosi.SATNOGS_TELEMETRY.format(norad_id),
                            headers=headers,
                            params=parameters,
                            allow_redirects=True)
    if(response.status_code == 200):
        if(len(response.json()) == 0):
            raise ValueError('No telemetry found for satellite with Norad ID: {}'
                             .format(norad_id))
        else:
            return response.json()[0]
    else:
        raise ValueError('Non-200 response from satnogs: {}'
                         .format(response))


def decode_telemetry_frame(telemetry_frame: bytes) -> csim.Csim.BeaconLong:
    """Takes a raw and encoded telemetry frame and decodes it according to a
    provided Kaitai Struct

    Parameters
    ----------
    telemetry_frame: `bytes` The encoded telemetry frame from satnogs

    Returns
    -------
    `csim.Csim.BeaconLong`: The decoder object with all of the aptly decoded\
    telemetry, *(only returns a `csim.Csim.BeaconLong` since it's the only\
    supportable decoder right now)*
    """
    payload = csim.Csim.from_bytes(telemetry_frame) \
                       .ax25_frame \
                       .payload \
                       .ax25_info
    return payload

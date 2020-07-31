import requests
import cosi.structs.csim as csim
from socket import gaierror
from pytz import utc
from datetime import datetime, \
                     timedelta
from dateutil.parser import parse
from cosi.common import SATNOGS_SATELITE, \
                    SATNOGS_TELEMETRY, \
                    SATNOGS_TOKEN, \
                    EnvironmentVariableNotDefined

STALE_FRAME_TIME = timedelta(days=1)


class NoDecoderForTelemetryFrame(Exception):
    """An error specification.
    This is thrown when a satellite is retrieved from Satnogs, but the decoder
    for it is unknown/unavailable, hence making it imposible to decode the
    telemetry frame.

    Attributes
    ---------
    args : Error details
        In-length details about what broke.
    """

    def __init__(self, args):
        super().__init__(self, "Decoder frame failure! \
                                Failed with arguments: " + str(args))
        self.args = args


class Satellite:
    """A data structure containing useful metadata about a satelite.

    Attributes
    ---------
    norad_id : Norad ID
        The unique satellite identifier.
    name :
        The satellite name.
    logo :
        A url to the satelite's logo (image).
    status :
        The satelites curent status.
    telemetries :
        A list of telemetry decoders.
    """
    norad_id: int
    name: str
    logo: str
    status: str
    telemetries: list


def get_age(first, second=datetime.now(utc)):
    """Gets the time difference of two different times.

    Parameters
    ----------
    first : The first date-time.
        A possbile pass.
    second : The second date-time.
        List of existing approved OrbitalPass objects to check against.

    Returns
    -------
    timedelta -- The time difference
    """
    return second - parse(first)


def request_satelite(norad_id=None):
    """Makes a request to satnogs.org for metadata on the satelite specified by
    Norad ID.

    Parameters
    ----------
    norad_id : Satellite Norad ID
        A unique satellite identifier.

    Returns
    -------
    Satelite -- A satellite data structure containing useful metadata about the
                satellite.
    """
    try:
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        parameters = {'format': 'json', 'norad_cat_id': str(norad_id)}
        return requests.get(SATNOGS_SATELITE.format(norad_id),
                            headers=headers,
                            params=parameters,
                            allow_redirects=True).json()
    except gaierror:
        return None


def request_telemetry(norad_id=None):
    """Makes a request to satnogs.org for the raw telemetry frame of the
    satelite specified by Norad ID.

    Parameters
    ----------
    norad_id : Satellite Norad ID
        A unique satellite identifier.

    Returns
    -------
    dict :
        -- norad_cat_id : Satellite Norad ID
        -- transmitter : ? (optional)
        -- app_source : ?
        -- schema : api schema (optional)
        -- decoded : ? (optional)
        -- frame : The raw and encoded telemetry frame
        -- timestamp : Time when the frame was constructed
    """
    if(SATNOGS_TOKEN is None):
        raise EnvironmentVariableNotDefined("SATNOGS_TOKEN")

    try:
        headers = {'Authorization': "Token " + SATNOGS_TOKEN,
                   'Content-Type': 'application/json'}
        parameters = {'format': 'json', 'norad_cat_id': str(norad_id)}
        return requests.get(SATNOGS_TELEMETRY.format(norad_id),
                            headers=headers,
                            params=parameters,
                            allow_redirects=True).json()
    except gaierror:
        return None


def decode_telemetry_frame(telemetry: dict):
    """Takes a raw and encoded telemetry frame and decodes it according to a
    provided Kaitai Struct

    Parameters
    ----------
    telemetry : The raw and encoded telemetry frame
    f_type : The frame decoder type [CURRENTLY ONLY CSIM IS SUPPORTED]

    Returns
    -------
    dict:
        -- norad_cat_id : Satellite Norad ID
    """
    frame = bytearray.fromhex(telemetry.get('frame'))
    payload = csim.Csim.from_bytes(frame).ax25_frame.payload.ax25_info

    if(payload is csim.Csim.BeaconLong):
        return payload
    else:
        return None

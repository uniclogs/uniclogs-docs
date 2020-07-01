import requests
from socket import gaierror
from pytz import utc
from datetime import datetime, \
                     timedelta
from dateutil.parser import parse
from .structs.csim import Csim
from .common import SATNOGS_SATELITE, \
                    SATNOGS_TELEMETRY, \
                    SATNOGS_TOKEN, \
                    EnvironmentVariableNotDefined

STALE_FRAME_TIME = timedelta(days=1)


class NoDecoderForTelemetryFrame(Exception):
    def __init__(self, args):
        super().__init__(self, "Decoder frame failure! \
                                Failed with arguments: " + str(args))
        self.args = args


def get_age(first, second=datetime.now(utc)):
    return second - parse(first)


def request_satelite(norad_id=None):
    try:
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        parameters = {'format': 'json', 'norad_cat_id': str(norad_id)}
        return requests.get(SATNOGS_SATELITE,
                            headers=headers,
                            params=parameters,
                            allow_redirects=True).json()
    except gaierror:
        return None


def request_telemetry(norad_id=None):
    if(SATNOGS_TOKEN is None):
        raise EnvironmentVariableNotDefined("SATNOGS_TOKEN")

    try:
        headers = {'Authorization': "Token " + SATNOGS_TOKEN,
                   'Content-Type': 'application/json'}
        parameters = {'format': 'json', 'norad_cat_id': str(norad_id)}
        return requests.get(SATNOGS_TELEMETRY,
                            headers=headers,
                            params=parameters,
                            allow_redirects=True).json()
    except gaierror:
        return None


def parse_telemetry_frame(telemetry, f_type=Csim):
    frame = bytearray.fromhex(telemetry.get('frame'))
    info = Csim.from_bytes(frame) .ax25_frame \
                                  .payload \
                                  .ax25_info
    if(type(f_type) is Csim and type(info) is Csim.BeaconLong):
        return info.filtered_speed_rpm3
    else:
        raise NoDecoderForTelemetryFrame(type(f_type),
                                         "No decoder found for telemetry frame!")

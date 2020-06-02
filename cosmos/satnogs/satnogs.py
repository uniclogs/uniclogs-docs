#!/usr/bin/env python3
import sys
import requests
import utilities as utils
import kaitaistruct
from socket import gaierror
from common import BASE_URL, \
                   API_TOKEN, \
                   TEMPLATE_SATELITE, \
                   TEMPLATE_TELEMETRY, \
                   TEMPLATE_STRUCTURE
from pytz import utc
from datetime import datetime, timedelta
from dateutil.parser import parse
from structs.csim import Csim

STALE_FRAME_TIME = timedelta(days=1)


def satelite_info_path(norad_id):
    return TEMPLATE_SATELITE.replace('NID', str(norad_id))


def telemetry_info_path(norad_id):
    return TEMPLATE_TELEMETRY.replace('NID', str(norad_id))


def satelite_struct_path(norad_id):
    return TEMPLATE_STRUCTURE.replace('NID', str(norad_id))


def get_age(first, second=datetime.now(utc)):
    return second - parse(first)


def get_satelite(norad_id=None):
    try:
        request_uri = '/api/satellites'
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        parameters = {'format': 'json', 'norad_cat_id': str(norad_id)}
        return requests.get(BASE_URL + request_uri,
                            headers=headers,
                            params=parameters,
                            allow_redirects=True).json()
    except gaierror:
        return None


def load_satelite(norad_id):
    try:
        satelite = utils.load_json(satelite_info_path(norad_id))
    except FileNotFoundError:
        satelite = get_satelite(norad_id)[0]
        utils.dump_json(satelite_info_path(norad_id), satelite)
    return satelite


def get_telemetry(norad_id=None):
    try:
        request_uri = '/api/telemetry'
        headers = {'Authorization': "Token " + API_TOKEN,
                   'Content-Type': 'application/json'}
        parameters = {'format': 'json', 'norad_cat_id': str(norad_id)}
        return requests.get(BASE_URL + request_uri,
                            headers=headers,
                            params=parameters,
                            allow_redirects=True).json()
    except gaierror:
        return None


def load_telemetry(norad_id):
    try:
        telemetry = utils.load_json(telemetry_info_path((norad_id)))
    except FileNotFoundError:
        telemetry = get_telemetry(norad_id)[0]
        utils.dump_json(telemetry_info_path(norad_id), telemetry)
    return telemetry


def parse_telemetry_frame(telemetry, f_type=Csim):
    frame = bytearray.fromhex(telemetry.get('frame'))
    info = Csim.from_bytes(frame) \
                                    .ax25_frame \
                                    .payload \
                                    .ax25_info
    if(type(f_type) is Csim and type(info) is Csim.BeaconLong):
        return info.filtered_speed_rpm3
    else:
        return None


def main(args):
    # Guarentee the cache dir exists
    utils.prime_cache()

    # # Get the satellite id(s)
    if(len(args) == 0):  # Get all satellite + telemetry
        pass
    else:  # Get specified satellite + telemetry
        norad_id = args[0]

        satelite = load_satelite(norad_id)
        print('Satelite info: ' + str(satelite))

        telemetry = load_telemetry(norad_id)
        print('Telemetry info: ' + str(telemetry))

        age = get_age(telemetry.get('timestamp'))
        if(age > STALE_FRAME_TIME):
            print('Telemetry is stale! Refetching...')
            telemetry = get_telemetry(norad_id)[0]
            utils.dump_json(telemetry_info_path(norad_id), telemetry)
        else:
            print("Telemetry is recent!")

        # Parse the telemetry frame data
        try:
            frame = parse_telemetry_frame(telemetry)
            if(frame is not None):
                print("Decoded frame: " + str(frame))
            else:
                print('Frame has unknown encoding!')
        except UnicodeDecodeError as e:
            utils.error(e)


if __name__ == "__main__":
    main(sys.argv[1:])

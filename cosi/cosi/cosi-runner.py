#!/usr/bin/env python3
import sys
import re
import time
import datetime
import argparse
import cosi.models as models
import cosi.satnogs as satnogs
import cosi.spacetrack as spacetrack


def parse_poll_interval(poll_interval: str) -> int:
    """Takes the arguments list and returns the total seconds CoSI needs to
    wait before polling spacetrack and satnogs again.

    Parameters
    ----------
    * args: `list` A python list of arguments pre-parsed by arg-parse

    Returns
    -------
    `int`: Time in seconds for CoSI to sleep

    Raises
    ------
    `ValueError`: Raises this if the user-input for `--poll-interval`
    does not match the patter `[0-9]+(d|h|m|s)`
    """
    if(re.match('[0-9]+d', poll_interval) is not None):
        timedelta = datetime.timedelta(days=int(poll_interval[:-1]))
    elif(re.match('[0-9]+h', poll_interval) is not None):
        timedelta = datetime.timedelta(hours=int(poll_interval[:-1]))
    elif(re.match('[0-9]+m', poll_interval) is not None):
        timedelta = datetime.timedelta(minutes=int(poll_interval[:-1]))
    elif(re.match('[0-9]+s', poll_interval) is not None):
        timedelta = datetime.timedelta(seconds=int(poll_interval[:-1]))
    else:
        raise ValueError('Bad poll interval value: {}.\
                        \n\tPoll interval must follow pattern: [0-9]+(d|h|m|s)\
                        \n\tEx: --poll-interval 12h or --poll-interval 30m'
                         .format(poll_interval))
    return timedelta.total_seconds()


def fetch_tle(args: list):
    tle = spacetrack.request_tle(args.norad_id)
    tle = models.TLE(header_text=tle.get('TLE_LINE0'),
                     first_line=tle.get('TLE_LINE1'),
                     second_line=tle.get('TLE_LINE2'))
    if(args.debug):
        print('\nInserting {} into db...'.format(tle))
    models.inject_tle(tle)


def fetch_satellite(args: list):
    satellite = satnogs.request_satellite(args.norad_id)
    if(args.debug):
        print('\nSatellite info: {}'.format(satellite))


def fetch_telemetry(args: list):
    # Get latest telemetry
    encoded_telemetry = satnogs.request_telemetry(args.norad_id)
    frame = bytearray.fromhex(encoded_telemetry.get('frame'))
    if(args.debug):
        print('\nEncoded telemetry: {}'.format(encoded_telemetry))

    # Decode telemetry
    decoded_telemetry = satnogs.decode_telemetry_frame(frame)
    if(args.debug):
        print('\nDecoded telemetry: {}'.format(decoded_telemetry))

    # Send data to the db
    try:
        magentometer_telemetry = models.Telemetry(invalid_count=decoded_telemetry.mag_invalid_count,
                                                  sensor_used=decoded_telemetry.mag_sensor_used,
                                                  vector_body_1=decoded_telemetry.mag_vector_body1,
                                                  vector_body_2=decoded_telemetry.mag_vector_body2,
                                                  vector_body_3=decoded_telemetry.mag_vector_body3,
                                                  vector_valid=decoded_telemetry.mag_vector_valid)
    except AttributeError as e:
        print('\nFailed to decode telemetry: {}'.format(e))
        return

    try:
        if(args.debug):
            print('Injecting telemetry into the DB: {}'
                  .format(magentometer_telemetry))
            status = models.inject_telemetry(magentometer_telemetry)
            if(args.debug and status):
                print('\nSuccesfully injected!')
            else:
                raise Exception('Failed to inject telemetry')
    except Exception:
        if(args.debug):
            print('\nFailed to inject telemetry frame into DB: {}'
                  .format(magentometer_telemetry))


def cycle(args):
    if(args.debug):
        print('\n\n[{}]: Starting a new poll-cycle for CoSI...'
              .format(time.ctime()))

    if(not args.no_tle):
        fetch_tle(args)
    if(not args.no_satellite):
        fetch_satellite(args)
    if(not args.no_telemetry):
        fetch_telemetry(args)

    if(args.latest_tle is not None):
        try:
            norad_id = int(args.latest_tle[0])
            tle = models.get_latest_tle_by_id(norad_id)
        except ValueError:
            satellite_name = args.latest_tle[0]
            tle = models.get_latest_tle_by_name(satellite_name)
        print('Latest TLE: {}'.format(tle))


def main(args: list) -> None:
    # Parse cmd line arguments
    parser = argparse.ArgumentParser(prog='cosi-runner',
                                     description='Daemon for CoSI.',
                                     allow_abbrev=False)
    parser.add_argument('--latest-tle',
                        dest='latest_tle',
                        nargs=1,
                        metavar=('(NORAD ID|SATELLITE NAME)'),
                        help='[Default: 43793 (CSim)] Displays the latest TLE\
                              stored in DART DB either by Norad ID or by\
                              satellite name')
    parser.add_argument('-n', '--norad-id',
                        dest='norad_id',
                        type=int,
                        default=43793,
                        help='[Default: 43793 (CSim)] Norad Satellite ID to\
                              use when fetching TLE and Telemetry')
    parser.add_argument('--no-satellite',
                        dest='no_satellite',
                        action='store_true',
                        default=False,
                        help='Disables fetching the latest satellite info from\
                              https://db.satnogs.org')
    parser.add_argument('--no-telemetry',
                        dest='no_telemetry',
                        action='store_true',
                        default=False,
                        help='Disables fetching the latest telemetry from\
                              https://db.satnogs.org')
    parser.add_argument('--no-tle',
                        dest='no_tle',
                        action='store_true',
                        default=False,
                        help='Disables fetching the latest Two Line Element\
                             (TLE) from https://space-track.org')
    parser.add_argument('-o', '--once',
                        dest='once',
                        action='store_true',
                        default=False,
                        help='Runs a cycle once instead of looping every poll\
                        interval')
    parser.add_argument('-p', '--poll-interval',
                        dest='poll_interval',
                        type=str,
                        default='30m',
                        help='[Default: 30m] Time interval at which CoSI polls\
                             spacetrack and satnogs for data')
    parser.add_argument('-v', '--verbose',
                        dest='debug',
                        action='store_true',
                        default=False,
                        help='Enable additional debug information')
    args = parser.parse_args(args)
    poll_interval = parse_poll_interval(args.poll_interval)

    if(args.once):
        cycle(args)
    else:
        while True:
            cycle(args)
            time.sleep(poll_interval)


if __name__ == "__main__":
    main(sys.argv[1:])

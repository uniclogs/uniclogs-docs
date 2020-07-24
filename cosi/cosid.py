#!/usr/bin/env python3
import os
import sys
import time
import signal
import ballcosmos.script as b
import cosi.models as models
import cosi.satnogs as satnogs
import cosi.spacetrack as spacetrack

POLL_INTERVAL = 1200


def cycle():
    norad_id = 43793
    print('\n\n-----------------------------\nStarting a new poll cycle at {}!\n'.format(time.ctime()))

    tle = spacetrack.request_tle(norad_id)
    print('\n\nTLE: ' + str(tle))

    print('\n\ninserting TLE into db...')
    # models.add_tle(tle)

    satellite = satnogs.request_satelite(norad_id)
    print('\n\nSatellite: ' + str(satellite))

    encoded_telemetry = satnogs.request_telemetry(norad_id)[0]
    status = {True: 'OK',
              False: 'ERR'}[encoded_telemetry != []
                            and encoded_telemetry is not None]
    print('\n\nTelemetry: ' + status)
    if(status == 'OK'):
        decoded_telemetry = satnogs.decode_telemetry_frame(encoded_telemetry)

        # Get data from DART
        packet = b.get_tlm_packet('ENGR_LINK', 'MAGNETOMETER')
        print('\n\nGot magentometer packets from DART: {}'.format(packet))

        # Send data to dart
        magentometer_telemetry = {
            'INVALID_COUNT': decoded_telemetry.mag_invalid_count,
            'SENSOR_USED': decoded_telemetry.mag_sensor_used,
            'VECTOR_BODY1': decoded_telemetry.mag_vector_body1,
            'VECTOR_BODY2': decoded_telemetry.mag_vector_body2,
            'VECTOR_BODY3': decoded_telemetry.mag_vector_body3,
            'VECTOR_VALID': decoded_telemetry.mag_vector_valid
        }
        try:
            print('\n\nInjecting telemetry into DART: {}'.format(magentometer_telemetry))
            b.inject_tlm('ENGR_LINK', 'MAGNETOMETER', item_hash=magentometer_telemetry)
            print('Succesfully injected!')
        except Exception:
            print('Failed to inject telemetry frame into DART: {}'.format(magentometer_telemetry))


def daemonize(stdout,
              stderr,
              stdin,
              pidfile,
              start_msg='Started CoSI daemon with pid: {}'):
    try:
        # Fork
        pid = os.fork()

        # Kill parent
        if(pid > 0):
            sys.exit(0)
    except OSError as e:
        sys.stderr.write('First fork failed ({}, {})'
                         .format(e.errno, e.stderr))
        sys.exit(-1)

    # Decouple from parent
    os.chdir('/')
    os.umask(0)
    os.setsid()

    try:
        # Fork
        pid = os.fork()

        # Kill parent
        if(pid > 0):
            sys.exit(0)
    except OSError as e:
        sys.stderr.write('Second fork failed ({}, {})'
                         .format(e.errno, e.stderr))
        sys.exit(-1)

    # Open file descriptors
    if(not stderr):
        stderr = stdout
    s_in = open(stdin, 'r')
    s_out = open(stdout, 'a+')
    s_err = open(stderr, 'a+')
    pid = str(os.getpid())
    sys.stderr.write('\n{}\n'.format(start_msg.format(pid)))
    sys.stderr.flush()

    if(pidfile):
        open(pidfile, 'w+').write('{}\n'.format(pid))

    # bind the file descriptors
    os.dup2(s_in.fileno(), sys.stdin.fileno())
    os.dup2(s_out.fileno(), sys.stdout.fileno())
    os.dup2(s_err.fileno(), sys.stderr.fileno())


def start_stop(action,
               stdout,
               stderr,
               stdin,
               pid_filepath):
    action = action.lower()
    try:
        pid_file = open(pid_filepath, 'r')
        pid = int(pid_file.read().strip())
    except IOError:
        pid = None

    if(action == 'start'):
        if(pid):
            sys.stderr.write('CoSI daemon is already running!')
            sys.exit(-1)
        daemonize(stdout,
                  stderr,
                  stdin,
                  pid_filepath)
        cycle()
    elif(action == 'stop' or action == 'restart'):
        if(not pid):
            sys.stderr.write('CoSI daemon is not running!')
            sys.exit(-1)

        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as e:
            e = str(e)

            if(e.find('No such process') > 0):
                os.remove(pid_filepath)
                if(action == 'stop'):
                    sys.exit(0)
                action == 'start'
                pid = None
            else:
                print('There was a problem stopping or restarting the service: {}'.format(e))
                sys.exit(-1)
    elif(action == 'demo'):
        cycle()


def main(args):
    if(len(args) == 0):
        print('usage: cosid.py [start|restart|stop]')
        sys.exit(-1)

    config_path = os.path.expanduser('~/.config/cosid/')
    os.makedirs(config_path, exist_ok=True)

    start_stop(args[0],
               config_path + 'info.log',
               config_path + 'error.log',
               '/dev/null',
               config_path + 'cosid.pid')


if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/env python3
import sys
# import daemon
import ballcosmos.script as b
import cosi.satnogs as satnogs
import cosi.spacetrack as spacetrack


def cycle(norad_id):
    tle = spacetrack.request_tle(norad_id)
    print('TLE: ' + str(tle))

    satellite = satnogs.request_satelite(norad_id)
    print('Satellite: ' + str(satellite))

    encoded_telemetry = satnogs.request_telemetry(norad_id)[0]
    status = {True: 'OK',
              False: 'ERR'}[encoded_telemetry != []
                            and encoded_telemetry is not None]
    print('Telemetry: ' + status)
    if(status == 'OK'):
        decoded_telemetry = satnogs.decode_telemetry_frame(encoded_telemetry)

        # Get data from DART
        packet = b.get_tlm_packet('ENGR_LINK', 'MAGNETOMETER')
        print('Got magentometer packets from DART: {}'.format(packet))

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
            b.inject_tlm('ENGR_LINK', 'MAGNETOMETER', item_hash=magentometer_telemetry)
            print('Succesfully injected telemetry frame into DART: {}'.format(magentometer_telemetry))
        except Exception:
            print('Failed to inject telemetry frame into DART: {}'.format(magentometer_telemetry))


def main(args):
    if(len(args) == 0):
        args = [43793]
        print('No Norad ID provided, defaulting to using CSIM!')
    for id in args:
        try:
            id = int(id)
        except ValueError:
            print('Norad ID must be an integer!')
            sys.exit(-1)
        cycle(id)


if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/env python3
import sys
# import daemon
import ballcosmos.script as b
import cosi.satnogs as satnogs
import cosi.spacetrack as spacetrack


def main(args):
    if(len(args) == 0):
        print('Expected Norad ID!')
        sys.exit(-1)

    try:
        norad_id = int(args[0])
    except ValueError:
        print('Norad ID must be an integer!')
        sys.exit(-1)

    print('Norad ID: ' + str(norad_id))

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
        print('Decoded Telemetry: ' + str(decoded_telemetry))
        b.inject_tlm('ENGR_LINK', 'TLM TEMPS TEMP1 = 300, TEMP2 = 400, TIMESTAMP = 00320203')


if __name__ == "__main__":
    main(sys.argv[1:])

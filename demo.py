#!/usr/bin/env python3
import sys
import cosi
import json


def spacetrack_example(norad_id):
    tle = cosi.spacetrack.request_tle(norad_id)
    print(str(norad_id) + ' TLE: ' + str(tle))


def satnogs_example(norad_id):
    satelite = cosi.satnogs.request_satelite(norad_id)
    print('Sateilte: ' + str(satelite))

    telemetry = cosi.satnogs.request_telemetry(norad_id)
    print('Telemetry: ' + str(telemetry))

    # Dump telemetry for inspection
    file = open('telem.json', 'w+')
    file.write(json.dumps(telemetry,
               skipkeys=False, ensure_ascii=True, check_circular=True,
               allow_nan=True, cls=None, indent=2, separators=None,
               default=None, sort_keys=True))
    file.close()


def main(args):
    if(len(args) == 0):
        return -1

    norad_id = args[0]
    spacetrack_example(norad_id)
    satnogs_example(norad_id)


if __name__ == "__main__":
    main(sys.argv[1:])

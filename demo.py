#!/usr/bin/env python3
import sys
import cosi
from cosi.models import TLE


def main(args):
    if (len(args) == 0):  # Default to CSIM-FD
        args = [43793]
    else:
        args = list(map(lambda x: int(x), args))

    for norad_id in args:
        csim = cosi.satnogs.request_satelite(norad_id)

        print(str(csim))

        telem = cosi.satnogs.request_telemetry(norad_id)

        print(str(telem))


if __name__ == "__main__":
    main(sys.argv[1:])

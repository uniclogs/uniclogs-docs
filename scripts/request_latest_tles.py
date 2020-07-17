#!/usr/bin/env python3
import sys; sys.path.append('..')
import cosi.cosi.spacetrack as spacetrack
import cosi.cosi.models as models


def main(args):
    if(len(args) == 0):
        norad_ids = [965, 43793, 25544]
    else:
        norad_ids = args

    for raw_id in norad_ids:
        try:
            norad_id = int(raw_id)
        except ValueError:
            print('Norad Id: \"{}\" must be an integer!'.format(raw_id))
            sys.exit(-1)

        raw_tle = spacetrack.request_tle(norad_id)
        tle = models.TLE(header_text=raw_tle.get('TLE_LINE0'),
                         first_line=raw_tle.get('TLE_LINE1'),
                         second_line=raw_tle.get('TLE_LINE2'))
        print('TLE: ' + str(tle))
        models.add_tle(tle)


if __name__ == "__main__":
    main(sys.argv[1:])

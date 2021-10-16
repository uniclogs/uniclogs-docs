#!/usr/bin/env python3
import sys; sys.path.append('..')
import datetime
import cosi.cosi.models as models
import pass_calculator.calculator as pc


def main(args):
    if(len(args) == 0):
        print('Expected one or more Satelite Names!')

    start_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=7)
    end_time = start_time + datetime.timedelta(days=30)
    eb_coordinates = (45.5098357, -122.6827152)  # Engineering Building coords
    print('Using coordinates for Engineering building: ' + str(eb_coordinates))

    for name in args:
        latest_tle = models.get_latest_tle(name)
        formatted_tle = [latest_tle.header_text,
                         latest_tle.first_line,
                         latest_tle.second_line]
        print('Latest TLE for {}:\n\t{}'.format(name, latest_tle))
        passes = pc.get_all_passes(tle=formatted_tle,
                                   lat_deg=eb_coordinates[0],
                                   long_deg=eb_coordinates[1],
                                   start_time_utc=start_time,
                                   end_time_utc=end_time)
        if(len(passes) == 0):
            print('No passes found for that range!')
        else:
            for op in passes:
                print('Pass: ' + str(op))

        raise NotImplementedError('Dumping pass requests into DartDB not available yet!')


if __name__ == "__main__":
    main(sys.argv[1:])

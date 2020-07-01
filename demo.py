#!/usr/bin/env python3
import sys
import cosi
import pass_calculator.calculator as pc
import json
from cosi.dart_db import DartDB
from datetime import datetime, \
                     timezone


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


def pass_calculator_example(tle: list,
                            latitude: int = 45.512778,
                            longitude: int = 122.685278,
                            elevation: int = 47.0,
                            start: datetime = datetime(2020, 5, 26, tzinfo=timezone.utc),
                            stop: datetime  = datetime(2020, 5, 29, tzinfo=timezone.utc)):
    return pc.get_all_passes(tle=tle,
                             lat_deg=latitude,
                             long_deg=longitude,
                             elev_m=elevation,
                             start_time_utc=start,
                             end_time_utc=stop)


def main(args):
    db = DartDB('localhost', 'cosmos', 'ivo', '')

    # tle = ["ISS (ZARYA)",
    #        "1 25544U 98067A   20147.68235988  .00000878  00000-0  23780-4 0  9990",
    #        "2 25544  51.6443  94.9049 0001567 359.6611  61.5558 15.49392416228680"]
    #
    # orbital_passes = pass_calculator_example(tle)
    # for p in orbital_passes:
    #     print("Pass at: {datetime:%Y-%m-%d %H:%M:%S} for {duration:4.1f} minutes".format(datetime=p.AOS_datetime_utc, duration=(p.LOS_datetime_utc - p.AOS_datetime_utc).total_seconds()/60))


if __name__ == "__main__":
    main(sys.argv[1:])

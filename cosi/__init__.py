#!/usr/bin/env python3
import sys
import utilities as utils
import satnogs as s
# import spacetrack as s


# norad_id = 25544 for ISS (ZARYA)
def main(args):
    # Guarentee the cache dir exists
    utils.prime_cache()

    # # Get the satellite id(s)
    if(len(args) == 0):  # Get all satellite + telemetry
        pass
    else:  # Get specified satellite + telemetry
        norad_id = args[0]

        satelite = s.load_satelite(norad_id)
        print('Satelite info: ' + str(satelite))

        telemetry = s.load_telemetry(norad_id)
        print('Telemetry info: ' + str(telemetry))

        age = s.get_age(telemetry.get('timestamp'))
        if(age > s.STALE_FRAME_TIME):
            print('Telemetry is stale! Refetching...')
            telemetry = s.get_telemetry(norad_id)[0]
            utils.dump_json(s.telemetry_info_path(norad_id), telemetry)
        else:
            print("Telemetry is recent!")

        # Parse the telemetry frame data
        try:
            frame = s.parse_telemetry_frame(telemetry)
            if(frame is not None):
                print("Decoded frame: " + str(frame))
            else:
                print('Frame has unknown encoding!')
        except UnicodeDecodeError as e:
            utils.error(e)


if __name__ == "__main__":
    main(sys.argv[1:])

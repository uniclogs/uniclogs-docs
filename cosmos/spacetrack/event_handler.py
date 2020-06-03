from skyfield.api import Topos, load, EarthSatellite


class Pass(object):
    """
    POD class for holding all info realated to a OreSat pass.
    """
    def __init__(self):
        # UTC datetime at Acquisition of Signal
        self.AOS_datetime = None
        # UTC datetime at Loss of Signal
        self.LOS_datetime = None
        # Azimuth
        self.AOS_azimuth = None
        # Azimuth at Loss of Signal
        self.LOS_azimuth = None
        # Altitude at Acquistion of Signal
        self.AOS_altitude = None
        # Altitude at Loss of Signal
        self.LOS_altitude = None


def get_all_passes(satellite=None, location=None, t0=None, t1=None, deg=0.0):
    """
    Get a list of all passes for a satellite and location for a time span.

    @param satellite Skyfield EarthSatellite object
    @param location Skyfield Topos object
    @param t0 Skyfield event start datetime
    @param t1 Skyfield event end datetime
    @param deg Horizon degrees

    @return list of pass objects
    """

    pass_list = []

    if (satellite is None) or (location is None) or (t0 is None) or (t1 is None):
        raise Exception("Input error")

    t, events = satellite.find_events(location, t0, t1, deg)

    for ti, event in zip(t, events):
        name = ("acquisition", "max", "loss")[event]

        if event == 0:
            new_pass = Pass()

            new_pass.AOS_datetime = ti.utc_datetime()
        elif event == 2:
            new_pass.LOS_datetime = ti.utc_datetime()

            pass_list.append(new_pass) # add pass to list

    return pass_list


def get_all_available_passes(approved_passes=None, satellite=None, location=None, t0=None, t1=None, deg=0.0):
    """
    Is a wrapper ontop of get_all_passes() that will remove all passes that
    overlap with existing approved_passes

    @param approved_passes List of pass objects
    @param satellite Skyfield EarthSatellite object
    @param location Skyfield Topos object
    @param t0 Skyfield event start datetime
    @param t1 Skyfield event end datetime
    @param deg Horizon degrees

    @return list of available pass objects
    """

    if approved_passes is None:
        raise Exception("No approved passes")

    possible_passes = get_all_passes(satellite, location, t0, t1, deg)
    passes = []

    for pp in possible_passes:
        available = True

        for ap in approved_passes:

            """
            Check to see if the end of the possible pass overlaps with start of the approved pass
            and also check to if the start of the possible pass overlaps with end of the approved pass
            """
            if (pp.AOS_datetime <= ap.AOS_datetime and pp.LOS_datetime > ap.AOS_datetime) \
                    or (pp.AOS_datetime < ap.LOS_datetime and pp.LOS_datetime <= ap.LOS_datetime):
                available = False
                break # no reason to check against any other approved_passes


        if available:
            passes.append(pp)

    return passes


if __name__ == "__main__":
    # NOTE example path estimation for uniclogs, remove once no longer needed

    # make satellite object from TLE
    ts = load.timescale()
    tle_header = "ISS (ZARYA)"
    tle_line1 = "1 25544U 98067A   20147.68235988  .00000878  00000-0  23780-4 0  9990"
    tle_line2 = "2 25544  51.6443  94.9049 0001567 359.6611  61.5558 15.49392416228680"
    satellite = EarthSatellite(tle_line1, tle_line2, tle_header, ts)

    # uniclogs at PSU location
    uniclogs_location = Topos(latitude_degrees=45.512778, longitude_degrees=122.685278, elevation_m=47.0)

    # start / end datetimes
    dt0 = ts.utc(2020, 5, 26)
    dt1 = ts.utc(2020, 5, 29)

    horizon_deg = 0.0

    passes = get_all_passes(satellite, uniclogs_location, dt0, dt1, horizon_deg)

    for p in passes:
        print("Pass at: {datetime:%Y-%m-%d %H:%M:%S} for {duration:4.1f} minutes".format(datetime=p.AOS_datetime, duration=(p.LOS_datetime - p.AOS_datetime).total_seconds()/60))


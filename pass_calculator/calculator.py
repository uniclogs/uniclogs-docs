from .orbitalpass import OrbitalPass
from skyfield.api import Topos, \
                         load, \
                         EarthSatellite
from datetime import datetime


_DATETIME_STR_FORMAT = "%Y/%m/%d %H:%M:%S"


def pass_overlap(new_pass, approved_passes):
    """Checks to see if the possible pass will overlap with an existing
    approved pass.

    Parameters
    ----------
    new_pass : OrbitalPass
        A possbile pass.
    approved_passes : [OrbitalPass]
        List of existing approved OrbitalPass objects to check against.

    Returns
    -------
    bool
        True if pass overlaps with an existing approved pass or False if no overlap
    """

    available = False

    # convert string to datetime objects
    np_AOS_dt = datetime.strptime(new_pass.AOS_datetime_utc, _DATETIME_STR_FORMAT)
    np_LOS_dt = datetime.strptime(new_pass.LOS_datetime_utc, _DATETIME_STR_FORMAT)

    for ap in approved_passes:
        # convert string to datetime objects
        ap_AOS_dt = datetime.strptime(ap.AOS_datetime_utc, _DATETIME_STR_FORMAT)
        ap_LOS_dt = datetime.strptime(ap.LOS_datetime_utc, _DATETIME_STR_FORMAT)

        """
        Check to see if the end of the possible pass overlaps with start of
        the approved pass and also check to if the start of the possible pass
        overlaps with end of the approved pass
        """
        if (np_AOS_dt <= ap_AOS_dt and np_LOS_dt > ap_AOS_dt) \
                or (np_AOS_dt < ap_LOS_dt and np_LOS_dt <= ap_LOS_dt):
            available = True # pass overlap with an approved pass
            break # no reason to check against any other approved passes

    return available


def get_all_passes(
        tle=None,
        lat_deg=None,
        long_deg=None,
        elev_m=0.0,
        horizon_deg=0.0,
        start_time_utc=None,
        end_time_utc=None,
        min_duration_s=0,
        approved_passes=[]):
    """Get a list of all passes for a satellite and location for a time span.

    Wrapper for Skyfield TLE ground station pass functions that produces an
    OrbitalPass object list of possible passes.

    Parameters
    ----------
    tle : [str]
        Can be [tle_line1, tle_line2] or [tle_header, tle_line1, tle_line2]
    lat_deg : float
        latitude of ground station in degrees
    long_deg : float
        longitude of ground station in degrees
    elev_m : float
        elevation of ground station in meters
    horizon_deg : float
        Minimum horizon degrees
    start_time_utc : datetime
        The start datetime wanted.
    end_time_utc : datetime
        The end datetime wanted.
    min_duration_s : int
        Minimum duration wanted
    approved_passes : [OrbitalPass]
        A list of OrbitalPass objects for existing approved passes.

    Raises
    ------
    AttributeError
        If any arg is missing.
    ValueError
        If the tle list is incorrect.

    Returns
    -------
    [OrbitalPass]
        List of OrbitalPass to that are available in the timespan.

    """

    if tle == None:
        raise AttributeError("Missing tle input\n")
    elif lat_deg == None:
        raise AttributeError("Missing lat_deg input\n")
    elif long_deg == None:
        raise AttributeError("Missing long_deg input\n")
    elif start_time_utc == None:
        raise AttributeError("Missing start_time_utc input\n")
    elif end_time_utc == None:
        raise AttributeError("Missing end_time_utc input\n")

    pass_list = []

    ts = load.timescale()
    t0 = ts.utc(start_time_utc)
    t1 = ts.utc(end_time_utc)

    # make topocentric object
    loc = Topos(lat_deg, long_deg, elev_m)
    loc = Topos(latitude_degrees=lat_deg,
            longitude_degrees=long_deg, elevation_m=elev_m)

    # make satellite object from TLE
    if len(tle) == 2:
        satellite = EarthSatellite(tle[0], tle[1], "", ts)
    elif len(tle) == 3:
        satellite = EarthSatellite(tle[1], tle[2], tle[0], ts)
    else:
        raise ValueError("Invalid tle string list\n")

    # find all events
    t, events = satellite.find_events(loc, t0, t1, horizon_deg)

    # make oritbal pass list
    for x in range(0, len(events)-3, 3):
        AOS_datetime_utc = t[x].utc_datetime()
        LOS_datetime_utc = t[x+2].utc_datetime()
        duration_s = (LOS_datetime_utc - AOS_datetime_utc).total_seconds() / 60

        if duration_s > min_duration_s:
            diff = satellite - loc
            topocentric = diff.at(t[x])
            AOS_alt, AOS_azi, AOS_dist = topocentric.altaz()

            new_pass = OrbitalPass(
                    lat_deg,
                    long_deg,
                    elev_m,
                    horizon_deg,
                    AOS_datetime_utc.strftime(_DATETIME_STR_FORMAT),
                    AOS_alt.degrees,
                    AOS_azi.degrees,
                    AOS_dist.km,
                    LOS_datetime_utc.strftime(_DATETIME_STR_FORMAT)
                    )

            if not pass_overlap(new_pass, approved_passes):
                pass_list.append(new_pass) # add pass to list

    return pass_list

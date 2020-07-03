from .orbitalpass import OrbitalPass
from skyfield.api import Topos, \
                         load, \
                         EarthSatellite


def _calc_topocentric(satellite, location, dt):
    """Calculates topocentric coordinates for a satellite at a datetime.

    Parametes
    ---------
    satellite : EarthSatellite
        Satellite object to use.
    location : Topos
        A location on earth to use.
    dt : ts
        A timescale to calculate topocentric coordinates.

    Returns
    -------
    altitude : str
        altitude in degress
    azimuth : str
        azimuth in degrees
    distance : float
        distance to satellite in kilometers

    https://rhodesmill.org/skyfield/earth-satellites.html#generating-a-satellite-position
    """

    diff = satellite -  location
    topocentric = diff.at(dt)
    return topocentric.altaz()


def _pass_overlap(new_pass, approved_passes):
    """Checks to see if the possible pass will overlap with an existing approved pass.

    Parameters
    ----------
    new_pass : Pass
        A possbile pass.
    approved_passes : list of Pass
        List of existing approved Pass objects to check against.

    Returns
    -------
    bool
        True -- pass overlaps with an existing approved pass.
        False -- no overlap
    """

    available = False

    for ap in approved_passes:
        """
        Check to see if the end of the possible pass overlaps with start of
        the approved pass and also check to if the start of the possible pass
        overlaps with end of the approved pass
        """
        if (new_pass.AOS_datetime <= ap.AOS_datetime and new_pass.LOS_datetime > ap.AOS_datetime) \
                or (new_pass.AOS_datetime < ap.LOS_datetime and new_pass.LOS_datetime <= ap.LOS_datetime):
            available = True # pass overlap with an approved pass
            break # no reason to check against any other approved passes

    return available


def get_all_passes(tle=None, lat_deg=None, long_deg=None, elev_m=0.0, horizon_deg=0.0, start_time_utc=None, end_time_utc=None, min_duration_s=0, approved_passes=[]):
    """Get a list of all passes for a satellite and location for a time span.

    Parameters
    ----------
    tle : list of str
        Can be [tle_line1, tle_line2] or [tle_line1, tle_line2, tle_header]
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
    approved_passes : list of Pass
    A list of Pass objects for existing approved passes.

    Raises
    ------
    AttributeError
        If any arg is missing.
    ValueError
        If the tle list is incorrect.

    Returns
    -------
    list of Pass

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
    loc = Topos(latitude_degrees=lat_deg, longitude_degrees=long_deg, elevation_m=elev_m)

    # make satellite object from TLE
    if len(tle) == 2:
        satellite = EarthSatellite(tle[0], tle[1], "", ts)
    elif len(tle) == 3:
        satellite = EarthSatellite(tle[1], tle[2], tle[0], ts)
    else:
        raise ValueError("Invalid tle string list\n")

    # find all events
    t, events = satellite.find_events(loc, t0, t1, horizon_deg)

    # fill the pass_list with event data
    for ti, event in zip(t, events):
        event_name = ("acquisition", "max", "loss")[event]

        if event_name == "acquisition":
            new_pass = OrbitalPass()
            new_pass.AOS_datetime_utc = ti.utc_datetime()
            new_pass.AOS_altitude, new_pass.AOS_azimuth, new_pass.AOS_distance = _calc_topocentric(satellite, loc, ti)
        elif event_name == "loss":
            new_pass.LOS_datetime_utc = ti.utc_datetime()
            new_pass.LOS_altitude, new_pass.LOS_azimuth, new_pass.LOS_distance = _calc_topocentric(satellite, loc, ti)

            if _pass_overlap(new_pass, approved_passes):
                continue # new pass overlap with an approved passes

            # check duration
            if ((new_pass.LOS_datetime_utc - new_pass.AOS_datetime_utc).total_seconds()/60) > min_duration_s:
                new_pass.gs_latitude = lat_deg
                new_pass.gs_longitude = long_deg
                new_pass.gs_elevation_m = elev_m
                new_pass.horizon_deg = horizon_deg
                pass_list.append(new_pass) # add pass to list

    return pass_list

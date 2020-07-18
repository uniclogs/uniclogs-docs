import datetime


class OrbitalPass():
    """POD class for holding all info realated to a pass.

    Attributes
    ----------
    gs_latitude_deg : float
        ground station latitude in decimal degrees
    gs_longitude_deg : float
        ground station longitude in decimal degrees
    aos_utc : datetime
        UTC datetime at AOS (acquisition of signal/satellite)
    los_utc : datetime
        UTC datetime at LOS (loss of signal/satellite)
    gs_elevation_m : float
        *optional* ground station elevation in meters
    horizon_deg : float
        *optional* horizon degrees
    """

    def __init__(self,
                 gs_latitude_deg,
                 gs_longitude_deg,
                 aos_utc,
                 los_utc,
                 gs_elevation_m=0.0,
                 horizon_deg=0.0):
        # type: (float, float, datetime, datetime, float, float) -> ()

        # Location data for the ground station
        self.gs_latitude_deg = gs_latitude_deg
        self.gs_longitude_deg = gs_longitude_deg
        self.gs_elevation_m = gs_elevation_m
        self.horizon_deg = horizon_deg

        # datetimes
        self.aos_utc = aos_utc
        self.los_utc = los_utc

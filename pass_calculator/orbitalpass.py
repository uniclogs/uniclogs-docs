class OrbitalPass():
    """POD class for holding all info realated to a pass.

    Attributes
    ----------
    gs_latitude : float
        ground station latitude in decimal degrees
    gs_longitude : float
        ground station long in decimal degrees
    gs_elevation_m : float
        ground station elevation in m
    horizon_deg : float
        horizon degrees
    AOS_datetime : datetime
        datetime at acquisition of signal
    AOS_azimuth : str
        azimuth string at acquisition of signal
    AOS_altitude : str
        altitude degrees string at acquisition of signal
    AOS_distance : int
        distance to satellite at acquistion of signal in m
    LOS_datetime : datetime
        datetime at loss of signal
    LOS_azimuth : str
        azimuth string at loss of signal
    LOS_altitude : str
        altitude degrees string at loss of signal
    LOS_distance : int
        distance to satellite at loss of signal in m
    """
    def __init__(self):
        # Location data for the ground station
        self.gs_latitude = 0.0
        self.gs_longitude = 0.0
        self.gs_elevation_m = 0.0
        self.horizon_deg = 0.0
        # Event data at Acquisition of Signal
        self.AOS_datetime_utc = None
        self.AOS_azimuth = None
        self.AOS_altitude = None
        self.AOS_distance = 0.0
        # Event data at Loss of Signal
        self.LOS_datetime_utc = None
        self.LOS_azimuth = None
        self.LOS_altitude = None
        self.LOS_distance = 0.0

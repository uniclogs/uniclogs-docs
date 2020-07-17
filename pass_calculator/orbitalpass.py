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
    AOS_datetime : str
        datetime at acquisition of signal
    AOS_azimuth : float
        azimuth at acquisition of signal
    AOS_altitude : float
        altitude degrees at acquisition of signal
    AOS_distance : float
        distance to satellite at acquistion of signal in kilometers
    LOS_datetime : str
        datetime at loss of signal
    """

    def __init__(self,
                 gs_latitude,
                 gs_longitude,
                 gs_elevation_m,
                 horizon_deg,
                 AOS_datetime_utc,
                 AOS_altitude,
                 AOS_azimuth,
                 AOS_distance,
                 LOS_datetime_utc):
        # type: (float, float, float, float, str, float, float, float, str)->()

        # Location data for the ground station
        self.gs_latitude = gs_latitude
        self.gs_longitude = gs_longitude
        self.gs_elevation_m = gs_elevation_m
        self.horizon_deg = horizon_deg
        # Event data at Acquisition of Signal
        self.AOS_datetime_utc = AOS_datetime_utc
        self.AOS_altitude = AOS_altitude
        self.AOS_azimuth = AOS_azimuth
        self.AOS_distance = AOS_distance
        # Event data at Loss of Signal
        self.LOS_datetime_utc = LOS_datetime_utc

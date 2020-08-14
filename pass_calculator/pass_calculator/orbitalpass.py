from datetime import timezone, datetime
import json


class OrbitalPass(object):
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
    gs_latitude_deg = 0.0
    gs_longitude_deg = 0.0
    gs_elevation_m = 0.0
    horizon_deg = 0.0

    RESTFUL_JSON = {
            "latitude": gs_latitude_deg,
            "longitude": gs_longitude_deg,
            "elevation_m": gs_elevation_m,
            "horizon_deg": horizon_deg,
            "aos_utc": "",
            "los_utc": ""
            }

    def __init__(self,
                 gs_latitude_deg: float,
                 gs_longitude_deg: float,
                 aos_utc: datetime,
                 los_utc: datetime,
                 gs_elevation_m=0.0,
                 horizon_deg=0.0):

        # Location data for the ground station
        self.gs_latitude_deg = gs_latitude_deg
        self.gs_longitude_deg = gs_longitude_deg
        self.gs_elevation_m = gs_elevation_m
        self.horizon_deg = horizon_deg

        # datetimes
        self.aos_utc = aos_utc
        self.los_utc = los_utc

    def __eq__(self, other):
        ret = True

        if self.gs_latitude_deg != other.gs_latitude_deg:
            ret = False
        elif self.gs_longitude_deg != other.gs_longitude_deg:
            ret = False
        elif self.gs_elevation_m != other.gs_elevation_m:
            ret = False
        elif self.horizon_deg != other.horizon_deg:
            ret = False
        elif self.aos_utc != other.aos_utc:
            ret = False
        elif self.los_utc != other.los_utc:
            ret = False

        return ret


class OrbitalPassJsonEncoder(json.JSONEncoder):
    """
    JSON encoder for orbital pass object.
    """

    def default(self, obj):
        if isinstance(obj, OrbitalPass):
            aos_str = obj.aos_utc.replace(tzinfo=timezone.utc).isoformat()
            los_str = obj.los_utc.replace(tzinfo=timezone.utc).isoformat()

            json_str = {
                    "latitude": obj.gs_latitude_deg,
                    "longitude": obj.gs_longitude_deg,
                    "elevation_m": obj.gs_elevation_m,
                    "horizon_deg": obj.horizon_deg,
                    "aos_utc": aos_str,
                    "los_utc": los_str
                    }

            return json_str

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

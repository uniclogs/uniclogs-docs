from datetime import timezone
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


class OrbitalPassJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OrbitalPass):
            json_str = {
                    "latitude": obj.gs_latitude_deg,
                    "longitude": obj.gs_longitude_deg,
                    "elevation_m": obj.gs_elevation_m,
                    "horizon_deg": obj.horizon_deg,
                    "aos_utc": obj.aos_utc.replace(tzinfo=timezone.utc).isoformat(),
                    "los_utc": obj.los_utc.replace(tzinfo=timezone.utc).isoformat()
                    }
            return json_str

         # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

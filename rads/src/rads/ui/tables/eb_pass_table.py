"""
The menu for selecting eb passes table.
"""

from datetime import datetime, timedelta
from rads.database.query import query_latest_tle
from rads.database.insert import insert_new_request
from pass_calculator.calculator import get_all_passes
from pass_calculator.orbitalpass import OrbitalPass

PSU_LAT = 45.512778
PSU_LONG = -122.685278
PSU_ELEV = 47.0
_DT_STR_FORMAT = "%Y/%m/%d %H:%M:%S"
_STR_FORMAT = "{:19} | {:19} | {:^3}"


class EBPass(OrbitalPass):
    """
    A nice wrapper class for expanding OrbitalPass to have a flag for add the
    pass.
    """

    def __init__(self, orbital_pass):
        super().__init__(
            orbital_pass.gs_latitude_deg,
            orbital_pass.gs_longitude_deg,
            orbital_pass.aos_utc,
            orbital_pass.los_utc,
            orbital_pass.gs_elevation_m,
            orbital_pass.horizon_deg
            )
        self.add = False

    def __str__(self):
        if self.add is True:
            add_status = "Y"
        else:
            add_status = " "

        return _STR_FORMAT.format(
            self.aos_utc.strftime(_DT_STR_FORMAT),
            self.los_utc.strftime(_DT_STR_FORMAT),
            add_status
            )


class EBPassTable():
    """
    A list of eb pass object that is used by eb requests.
    """

    def __init__(self):
        tle = query_latest_tle()
        now = datetime.utcnow()
        future = datetime.now() + timedelta(days=7)
        eb_passes = get_all_passes(
            tle,
            PSU_LAT,
            PSU_LONG,
            now,
            future
            )
        self.header = _STR_FORMAT.format("AOS", "LOS", "Add")
        self.data = []
        for p in eb_passes:  # TODO look for existing passes
            self.data.append(EBPass(p))

        self.data_len = len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return self.data_len

    def save(self):
        """
        save changes to db
        """
        for d in self.data:
            if d.add is True:
                insert_new_request(d)

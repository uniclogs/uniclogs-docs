from db_interface import query_upcomming_requests, update_approve_deny
from request_data import RequestData
import reverse_geocoder as rg

_DT_STR_FORMAT = "%Y/%m/%d %H:%M:%S"
_STR_FORMAT = "{:7} | {:8} | {:15} | {:^5} | {:19} | {:19} | {:30}"


class Request(RequestData):
    def __init__(self, request):
        super().__init__(
                request.id,
                request.user_token,
                request.pass_id,
                request.is_approved,
                request.is_sent,
                request.created_dt,
                request.updated_dt,
                request.observation_type,
                request.pass_data.gs_latitude_deg,
                request.pass_data.gs_longitude_deg,
                request.pass_data.gs_elevation_m,
                request.pass_data.aos_utc,
                request.pass_data.los_utc
                )
        self.deny_count = 0

    def __str__(self):

        obs_type = self.observation_type
        if obs_type is None:
            obs_type = " "

        if self.is_approved is True:
            ad_status = "approved"
        elif self.is_approved is False:
            ad_status = "denied"
        else:
            ad_status = "pending"

        if self._is_sent is True:
            sent_status = "Y"
        else:
            sent_status = "N"

        if self.geo is not None:
            loc = self.geo["name"] + ", " + self.geo["admin1"]
        else:
            loc = " "

        return _STR_FORMAT.format(
                self.id,
                ad_status,
                obs_type,
                sent_status,
                self.pass_data.aos_utc.strftime(_DT_STR_FORMAT),
                self.pass_data.los_utc.strftime(_DT_STR_FORMAT),
                loc
                )

    def deny(self):
        self.deny_count += 1
        self.is_approved = False

    def undeny(self):
        if self.deny_count > 0:
            self.deny_count -= 1
            if self.deny_count == 0:
                self.is_approved = True


class RequestTable():
    def __init__(self):
        self.data = []
        coordinates = []

        requests = query_upcomming_requests()
        for r in requests:
            self.data.append(Request(r))
            coor = (r.pass_data.gs_latitude_deg,  r.pass_data.gs_longitude_deg)
            coordinates.append(coor)

        locations = rg.search(coordinates, verbose=False)

        for i in range(len(self.data)):
            self.data[i].geo = locations[i]

        self.data_len = len(self.data)
        self.header = _STR_FORMAT.format(
                "ID",
                "Status",
                "Type",
                "Sent",
                "AOS",
                "LOS",
                "City, State"
                )

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return self.data_len

    def save(self):
        update_approve_deny(self.data)

from datetime import datetime, timezone
import pass_calculator as pc


# ISS TLE
TEST_TLE_HEADER = "ISS (ZARYA)"
TEST_TLE_LINE_1 = "1 25544U 98067A   20199.71986111 -.00000291  00000-0  28484-5 0  9999"
TEST_TLE_LINE_2 = "2 25544  51.6429 197.3485 0001350 125.7534 225.4894 15.49513771236741"


# location data for Portland State
PSU_LAT = 45.512778
PSU_LONG = -122.685278
PSU_ELEV = 47.0


pass_list = pc.get_all_passes(
        tle=[TEST_TLE_HEADER, TEST_TLE_LINE_1, TEST_TLE_LINE_2],
        lat_deg=PSU_LAT,
        long_deg=PSU_LONG,
        start_datetime_utc=datetime(2020, 7, 17, tzinfo=timezone.utc),
        end_datetime_utc=datetime(2020, 7, 24, tzinfo=timezone.utc),
        elev_m=PSU_ELEV
        )


for p in pass_list:
    print("{} {} {} {} {} {}".format(
        p.gs_latitude_deg,
        p.gs_longitude_deg,
        p.gs_elevation_m,
        p.horizon_deg,
        p.aos_utc,
        p.los_utc
        ))

from datetime import datetime, timezone
import sys; sys.path.append("..")
import pass_calculator as pc

# ISS TLE
TEST_TLE_HEADER = "ISS (ZARYA)"
TEST_TLE_LINE_1 = "1 25544U 98067A   20199.71986111 -.00000291  00000-0  28484-5 0  9999"
TEST_TLE_LINE_2 = "2 25544  51.6429 197.3485 0001350 125.7534 225.4894 15.49513771236741"

# location data for Portland State
PSU_LAT = 45.512778
PSU_LONG = -122.685278
PSU_ELEV = 47.0


def test_get_all_passes():
    # no approved passes
    pass_list = pc.get_all_passes(
            tle = [TEST_TLE_HEADER, TEST_TLE_LINE_1, TEST_TLE_LINE_2],
            lat_deg = PSU_LAT,
            long_deg = PSU_LONG,
            start_datetime_utc = datetime(2020, 7, 17, tzinfo=timezone.utc),
            end_datetime_utc = datetime(2020, 7, 24, tzinfo=timezone.utc),
            elev_m = PSU_ELEV
            )

    assert len(pass_list) == 45

    # some approved passes
    pass_list2 = pc.get_all_passes(
            tle = [TEST_TLE_HEADER, TEST_TLE_LINE_1, TEST_TLE_LINE_2],
            lat_deg = PSU_LAT,
            long_deg = PSU_LONG,
            start_datetime_utc = datetime(2020, 7, 17, tzinfo=timezone.utc),
            end_datetime_utc = datetime(2020, 7, 24, tzinfo=timezone.utc),
            elev_m = PSU_ELEV,
            approved_passes = pass_list[:10]
            )

    assert len(pass_list2) == 35

    # no approved passes with a 10 minutes minimum duration
    pass_list3 = pc.get_all_passes(
            tle = [TEST_TLE_HEADER, TEST_TLE_LINE_1, TEST_TLE_LINE_2],
            lat_deg = PSU_LAT,
            long_deg = PSU_LONG,
            start_datetime_utc = datetime(2020, 7, 17, tzinfo=timezone.utc),
            end_datetime_utc = datetime(2020, 7, 24, tzinfo=timezone.utc),
            elev_m = PSU_ELEV,
            min_duration_s = 600
            )

    assert len(pass_list3) == 32

    # no approved passes with a 10 minutes minimum duration
    pass_list3 = pc.get_all_passes(
            tle = [TEST_TLE_HEADER, TEST_TLE_LINE_1, TEST_TLE_LINE_2],
            lat_deg = PSU_LAT,
            long_deg = PSU_LONG,
            start_datetime_utc = datetime(2020, 7, 17, tzinfo=timezone.utc),
            end_datetime_utc = datetime(2020, 7, 24, tzinfo=timezone.utc),
            elev_m = PSU_ELEV,
            horizon_deg = 15.0
            )

    assert len(pass_list3) == 34



def test_validate_pass():

    # get some valid passes for tests
    pass_list = pc.get_all_passes(
            tle = [TEST_TLE_HEADER, TEST_TLE_LINE_1, TEST_TLE_LINE_2],
            lat_deg = PSU_LAT,
            long_deg = PSU_LONG,
            start_datetime_utc = datetime(2020, 7, 17, tzinfo=timezone.utc),
            end_datetime_utc = datetime(2020, 7, 24, tzinfo=timezone.utc),
            elev_m = PSU_ELEV
            )

    # check valid pass
    ret = pc.validate_pass(
            tle = [TEST_TLE_HEADER, TEST_TLE_LINE_1, TEST_TLE_LINE_2],
            orbital_pass = pass_list[13] # pick a random valid pass
            )

    assert ret == True

    # make invalid pass
    invalid_orbital_pass= pc.OrbitalPass(
            gs_latitude_deg = PSU_LAT,
            gs_longitude_deg = PSU_LONG,
            aos_utc = datetime(2020, 7, 23, hour=10, minute=44, second=31, tzinfo=timezone.utc),
            los_utc = datetime(2020, 7, 23, hour=10, minute=53, second=25, tzinfo=timezone.utc),
            gs_elevation_m = PSU_ELEV
            )

    # check invalid pass
    ret2 = pc.validate_pass(
            tle = [TEST_TLE_HEADER, TEST_TLE_LINE_1, TEST_TLE_LINE_2],
            orbital_pass = invalid_orbital_pass,
            )

    assert ret2 == False

import sys; sys.path.append('..')
import os
import pytest
import cosi
import cosi.spacetrack as spacetrack


def test_request_tle_is_not_none():
    """Given a valid `norad_id`, when polling spacetrack for latest TLE, then
    the result should be a non-null dictionary with three string values
    """
    norad_id = 965
    res = spacetrack.request_tle(norad_id)
    assert res is not None
    assert res.get('TLE_LINE0') is not None
    assert res.get('TLE_LINE1') is not None
    assert res.get('TLE_LINE2') is not None


def test_request_tle_raises_error_on_bad_norad_id():
    """Given an invalid `norad_id`, when polling spacetrack for latest TLE,
    then the function should raise a TLERequestFailed exception
    """
    norad_id = -1
    with pytest.raises(spacetrack.TLERequestFailed):
        spacetrack.request_tle(norad_id)


def test_request_tle_raises_error_on_no_username():
    """Given no username, when polling spacetrack for latest TLE, then the
    function should raise an EnvironmentError exception
    """
    norad_id = 965
    cosi.SPACETRACK_USERNAME = None
    with pytest.raises(EnvironmentError):
        spacetrack.request_tle(norad_id)


def test_request_tle_raises_error_on_no_password():
    """Given no password, when polling spacetrack for latest TLE, then the
    function should raise an EnvironmentError exception
    """
    norad_id = 965
    cosi.SPACETRACK_PASSWORD = None
    with pytest.raises(EnvironmentError):
        spacetrack.request_tle(norad_id)


def test_request_tle_raises_error_on_bad_username():
    """Given an invalid username, when polling spacetrack for latest TLE, then
    the function should raise an TLERequestFailed exception
    """
    norad_id = 965
    cosi.SPACETRACK_USERNAME = 'badusername'
    cosi.SPACETRACK_PASSWORD = os.getenv('SPACETRACK_PASSWORD')
    with pytest.raises(spacetrack.TLERequestFailed):
        spacetrack.request_tle(norad_id)


def test_request_tle_raises_error_on_bad_password():
    """Given an invalid password, when polling spacetrack for latest TLE, then
    the function should raise an TLERequestFailed exception
    """
    norad_id = 965
    cosi.SPACETRACK_USERNAME = os.getenv('SPACETRACK_USERNAME')
    cosi.SPACETRACK_PASSWORD = 'badpassword'
    with pytest.raises(spacetrack.TLERequestFailed):
        spacetrack.request_tle(norad_id)

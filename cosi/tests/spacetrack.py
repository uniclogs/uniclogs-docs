import sys
sys.path.append('../')
import cosi


def test_request_tle_is_not_none():
    res = cosi.spacetrack.request_tle(965)
    assert res is not None

import sys; sys.path.append('..')
import pytest
import cosi.satnogs as satnogs
import cosi.structs as structs
import datetime


def test_get_age_is_valid():
    """Given two valid datetimes, when getting the age between the two, the
    result should be a valid and correct timedelta
    """
    first = datetime.datetime(year=2020, month=1, day=15)
    second = datetime.datetime(year=2020, month=2, day=14)
    assert satnogs.get_age(first, second) == datetime.timedelta(days=30)


def test_request_satellite_is_not_none():
    """Given a valid `norad_id`, when polling satnogs for satellite data,
    then the result should be a vaild dict with satellite data
    """
    norad_id = 43793  # Csim FD Satellite
    satellite = satnogs.request_satellite(norad_id)
    assert satellite is not None


@pytest.mark.skip(reason='Satnogs API being inconsistent?')
def test_request_telemetry_is_not_none():
    """Given a valid `norad_id`, when polling satnogs for telemetry data,
    then the result should be a vaild dict with telemetry data
    """
    norad_id = 43793  # Csim FD Satellite
    telemetry = satnogs.request_telemetry(norad_id)
    assert telemetry is not None
    assert telemetry.get('frame') is not None


def test_request_telemetry_raises_error():
    """Given a valid telemetry frame from a satellite that does not support
    Kaitai structs, when polling satnogs for telemetry data, then the function
    should raise a ValueError
    """
    norad_id = 965  # TRANSPORT Satellite
    with pytest.raises(ValueError):
        satnogs.request_telemetry(norad_id)


def test_decode_telemetry_is_not_none():
    """Given a valid telemetry frame from a satellite that supports Kaitai
    structs, when polling satnogs for telemetry data, then the result should
    be a vaild Csim.BeaconLong object
    """
    norad_id = 43793  # Csim FD Satellite
    telemetry = satnogs.request_telemetry(norad_id)
    frame = bytearray.fromhex(telemetry.get('frame'))
    decoded_telemetry = satnogs.decode_telemetry_frame(frame)
    assert decoded_telemetry is not None
    assert isinstance(decoded_telemetry, structs.csim.Csim.BeaconLong)

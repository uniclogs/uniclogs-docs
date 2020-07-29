import sys
sys.path.insert(0, '..')
from models import Request, Pass, Tle, Session, PassRequest
from datetime import datetime, timezone, timedelta
import random, string
sys.path.insert(0, '../..')
import pass_calculator.calculator as pc


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# get latest LTE and approved passes list from DB
tle = [
    "1 25544U 98067A   20185.75040611  .00000600  00000-0  18779-4 0  9992",
    "2 25544  51.6453 266.4797 0002530 107.7809  36.4383 15.49478723234588"
    ]

latitude = 44.0533
longitude = -121.3345
elevation_m = 100.0

now = datetime.now()
now = now - timedelta(days=1)
now = now.replace(tzinfo=timezone.utc)
future = now + timedelta(days=7)
future = future.replace(tzinfo=timezone.utc)

session = Session()

# call pass calculator
orbital_passes = pc.get_all_passes(
        tle=tle,
        lat_deg=latitude,
        long_deg=longitude,
        start_datetime_utc=now,
        end_datetime_utc=future,
        elev_m=elevation_m
        )

for op in orbital_passes:
    new_pass = Pass(
        latitude=op.gs_latitude_deg,
        longtitude=op.gs_longitude_deg,
        elevation=op.gs_elevation_m,
        start_time=op.aos_utc,
        end_time=op.los_utc
        )

    session.add(new_pass)
    session.flush()

    new_request = Request(
        user_token=randomword(10),
        is_approved=random.choice([True, False, None]),
        is_sent=random.choice([True, False]),
        pass_uid=new_pass.uid
        )

    session.add(new_request)
    session.flush()

    new_pass_request = PassRequest(
            pass_id=new_pass.uid,
            req_token=new_request.user_token
            )

    session.add(new_pass_request)
    session.flush()

session.commit()
session.close()

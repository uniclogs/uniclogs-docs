"""
A nice place to hold all database insert functions.
"""

import string
import random
from .models import Request, Pass, Session


def _randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def insert_new_request(new_pass):
    """
    Inset new uniclogs passes into db.
    """
    session = Session()

    # look for pass in db
    result = session.query(Pass)\
        .with_lockmode('read')\
        .filter(Pass.start_time == new_pass.aos_utc,
                Pass.latitude == new_pass.gs_latitude_deg,
                Pass.longitude == new_pass.gs_longitude_deg)\
        .first()

    if result is None:  # pass not in db, add it
        new_pass = Pass(
            latitude=new_pass.gs_latitude_deg,
            longitude=new_pass.gs_longitude_deg,
            elevation=new_pass.gs_elevation_m,
            start_time=new_pass.aos_utc,
            end_time=new_pass.los_utc
            )

        session.add(new_pass)
        session.flush()

        pass_uid = new_pass.uid
    else:  # pass already in db
        pass_uid = result.uid

    new_request = Request(
        user_token=_randomword(20),  # TODO change this, env var?
        is_approved=True,
        is_sent=False,
        pass_uid=pass_uid,
        observation_type="uniclogs"
        )

    ret = new_request.uid

    # TODO send to COSMOS
    if True:  # TODO cosmos send worked
        new_request.is_sent = True

    session.add(new_request)
    session.commit()
    session.close()

    return ret

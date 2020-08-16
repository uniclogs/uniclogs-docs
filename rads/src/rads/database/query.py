"""
A nice place to hold all database query functions.
"""

from datetime import datetime
from sqlalchemy import func, exc
from loguru import logger
import reverse_geocoder as rg
from pass_calculator.calculator import pass_overlap
from .models import Request, Pass, Tle, Session
from .request_data import RequestData


def _fill_request_data(results):
    """
    Make a RequestData object for a Pass and Request models join.

    Parameters
    ----------
    requests
        A list of Request models joined with Pass models

    Returns
    -------
    [RequestData]
        A list of RequestData obj to be used by the ncruses.
    """

    requests = []
    coordinates = []

    for r in results:
        rd = RequestData(
            r.uid,
            r.user_token,
            r.pass_uid,
            r.is_approved,
            r.is_sent,
            r.created_date,
            r.updated_date,
            r.observation_type,
            r.pass_data.latitude,
            r.pass_data.longitude,
            r.pass_data.elevation,
            r.pass_data.start_time,
            r.pass_data.end_time,
            )
        requests.append(rd)

    if requests:
        # find nearest city, county, state, country info for anything in list

        for r in requests:
            coor = (r.pass_data.gs_latitude_deg,  r.pass_data.gs_longitude_deg)
            coordinates.append(coor)

        # NOTE this is way faster to do all at once, then one at a time.
        loc = rg.search(coordinates, verbose=False)

        for i in range(len(requests)):
            requests[i].geo = loc[i]

    return requests


def query_new_requests():
    """
    Queries all the new requests (NULL for is_approved).

    Returns
    -------
    [RequestData]
        A list of all new pass requests in acending created datetime order.
    """

    ret = []
    approved_req = []
    session = Session()

    try:
        result = session.query(Request)\
            .with_lockmode('read')\
            .join(Pass, Pass.uid == Request.pass_uid)\
            .filter(Pass.start_time > datetime.utcnow(),
                    Request.is_approved.is_(None))\
            .order_by(Request.created_date.asc())\
            .all()
        ret = _fill_request_data(result)
    except exc.SQLAlchemyError:
        logger.critical("New requests query failed {}".format(
            exc.SQLAlchemyError
            ))
    finally:
        session.close()

    # find all overlap for approved request in db
    approved_req = query_upcomming_requests()
    for r in ret:
        for a in approved_req:
            if pass_overlap(a.pass_data, [r.pass_data]) is True:
                r.db_approved_overlap.append(a.id)

    # find all overlap for new request
    for i in range(len(ret)):
        for j in range(i):
            if pass_overlap(ret[i].pass_data, [ret[j].pass_data]) is True:
                ret[i].new_overlap.append(ret[j].id)
                ret[j].new_overlap.append(ret[i].id)

    return ret


def query_upcomming_requests():
    """
    Queries all the archived requests.

    Returns
    -------
    [RequestData]
        A list of upcomming approved pass requests in acending AOS order.
    """

    ret = []
    session = Session()

    try:
        result = session.query(Request)\
            .with_lockmode('read')\
            .join(Pass, Pass.uid == Request.pass_uid)\
            .filter(Pass.start_time > datetime.utcnow(),
                    Request.is_approved.is_(True))\
            .order_by(Pass.start_time.asc())\
            .all()
    except exc.SQLAlchemyError:
        logger.critical("Upcomming requests query failed {}".format(
            exc.SQLAlchemyError
            ))
    finally:
        ret = _fill_request_data(result)
        session.close()

    return ret


def query_archived_requests():
    """
    Queries all the archived requests.

    Returns
    -------
    [RequestData]
        A list of archive pass requests in descending AOS order.
    """

    ret = []
    session = Session()

    try:
        result = session.query(Request)\
            .with_lockmode('read')\
            .join(Pass, Pass.uid == Request.pass_uid)\
            .filter(Pass.start_time <= datetime.utcnow())\
            .order_by(Pass.start_time.desc())\
            .all()
    except exc.SQLAlchemyError:
        logger.critical("Archive requests query failed {}".format(
            exc.SQLAlchemyError
            ))
    finally:
        ret = _fill_request_data(result)
        session.close()

    return ret


def query_latest_tle():
    """
    Get the latest tle from db.

    Returns
    -------
    [str]
        TLE data in the format of [tle_line1, tle_line2]
    """
    tle = []
    session = Session()

    try:
        # NOTE locking this will error and doesn't need to be atomic
        latest_tle_time = session.query(func.max(Tle.time_added))\
            .one()

        latest_tle = session.query(Tle)\
            .with_lockmode('read')\
            .filter(Tle.time_added == latest_tle_time)\
            .one()

        tle = [latest_tle.first_line, latest_tle.second_line]
    except exc.SQLAlchemyError:
        logger.critical("TLE query failed {}".format(exc.SQLAlchemyError))
    finally:
        session.close()

    return tle

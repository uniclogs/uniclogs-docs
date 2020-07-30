from models import Request, Pass, Tle, Session
from request_data import RequestData
from datetime import datetime
from sqlalchemy import func, exc


def _fill_request_data(result):
    """
    Make a RequestData object for a Pass and Request models join.

    Parameters
    ----------
    result
        A list of Request models joined with Pass models

    Returns
    -------
    [RequestData]
        A list of RequestData obj to be used by the ncruses.
    """

    requests = []

    for r in result:
        rd = RequestData(
                r.user_token,
                r.pass_uid,
                r.is_approved,
                r.is_sent,
                r.created_date,
                r.observation_type,
                r.pass_data.latitude,
                r.pass_data.longtitude,
                r.pass_data.elevation,
                r.pass_data.start_time,
                r.pass_data.end_time
                )
        requests.append(rd)

    return requests


def query_new_requests():
    """
    Queries all the new requests (NULL for is_approved).

    Returns
    -------
    [RequestData]
        A list of all new pass requests in acending created datetime order.
    """

    session = Session()

    # TODO get lock

    result = session.query(Request)\
        .join(Pass, Pass.uid == Request.pass_uid)\
        .filter(Pass.start_time > datetime.utcnow(),
                Request.is_approved.is_(None))\
        .order_by(Request.created_date.asc())\
        .all()

    ret = _fill_request_data(result)

    # TODO release lock

    session.close()

    return ret


def query_upcomming_requests():
    """
    Queries all the archived requests.

    Returns
    -------
    [RequestData]
        A list of upcomming approved pass requests in acending AOS order.
    """

    session = Session()

    # TODO get lock

    result = session.query(Request)\
        .join(Pass, Pass.uid == Request.pass_uid)\
        .filter(Pass.start_time > datetime.utcnow(),
                Request.is_approved.is_(True))\
        .order_by(Pass.start_time.asc())\
        .all()

    ret = _fill_request_data(result)

    # TODO release lock

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

    session = Session()

    # TODO get lock

    result = session.query(Request)\
        .join(Pass, Pass.uid == Request.pass_uid)\
        .filter(Pass.start_time <= datetime.utcnow())\
        .order_by(Pass.start_time.desc())\
        .all()

    ret = _fill_request_data(result)

    # TODO release lock

    session.close()

    return ret


def update_approve_deny(request_list):
    """
    Update request in th db to be approved or denied.

    Parameter
    ---------
    request_list: RequestData
        A list of requests to update
    """

    session = Session()

    # TODO get lock

    for r in request_list:
        if r.updated is False:
            continue

        try:
            # find the matching reuqest
            result = session.query(Request)\
                .join(Pass, Pass.uid == Request.pass_uid)\
                .filter(Request.user_token == r.user_token and
                        r.pass_id == Pass.uid)\
                .one()
        except exc.SQLAlchemyError:
            continue  # TODO log

        # make sure request/pass data has not changed
        if result.pass_data.start_time == r.pass_data.aos_utc and \
                result.pass_data.end_time == r.pass_data.los_utc:
            result.is_approved = r.is_approved

    session.commit()

    # TODO release lock

    session.close()


def query_tle():
    """
    Get the latest tle from db.

    Returns
    -------
    [str]
        TLE data in the format of [tle_line1, tle_line2]
    """
    session = Session()

    # TODO get lock

    latest_tle_time = session.query(func.max(Tle.time_added)).one()
    latest_tle = session.query(Tle)\
        .filter(Tle.time_added == latest_tle_time)\
        .one()

    tle = [latest_tle.first_line, latest_tle.second_line]

    # TODO release lock

    session.close()

    return tle

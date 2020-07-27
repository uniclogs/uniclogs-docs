from models import Request, Pass, Tle, Session
from request_data import RequestData, RequestHeader
from datetime import datetime


def _fill_request_data(result):

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
    session = Session()

    #TODO get lock

    result = session.query(Request)\
            .join(Pass, Pass.uid == Request.pass_uid)\
            .filter(Pass.start_time > datetime.utcnow(), Request.is_approved.is_(None))\
            .order_by(Request.created_date.asc())\
            .all()

    ret = _fill_request_data(result)

    #TODO release lock

    session.close()

    return ret


def query_upcomming_requests():
    session = Session()

    #TODO get lock

    result = session.query(Request)\
            .join(Pass, Pass.uid == Request.pass_uid)\
            .filter(Pass.start_time > datetime.utcnow())\
            .order_by(Request.created_date.asc())\
            .all()

    ret = _fill_request_data(result)

    #TODO release lock

    session.close()

    return ret


def query_archived_requests():
    session = Session()

    #TODO get lock

    result = session.query(Request)\
            .join(Pass, Pass.uid == Request.pass_uid)\
            .filter(Pass.start_time <= datetime.utcnow())\
            .order_by(Request.created_date.asc())\
            .all()

    ret = _fill_request_data(result)

    #TODO release lock

    session.close()

    return ret


def update_approve_deny(request_list):
    """
    """

    session = Session()

    #TODO get lock

    for r in request_list:
        if r.updated == False:
            continue

        try:
            # find the matching reuqest
            result = session.query(Request)\
                .join(Pass, Pass.uid == Request.pass_uid)\
                .filter(Request.user_token == r.user_token and
                        r.pass_id == Pass.uid)\
                .one()
        except:
            print("query failed")
            continue


        # make sure request/pass data has not changed
        print("{} {} {} {}".format(result.pass_data.start_time, r.pass_data.aos_utc, result.pass_data.end_time,  r.pass_data.los_utc))
        if result.pass_data.start_time == r.pass_data.aos_utc and result.pass_data.end_time == r.pass_data.los_utc:
            print("hi")
            result.is_approved = r.is_approved

    session.commit()

    #TODO release lock

    session.close()


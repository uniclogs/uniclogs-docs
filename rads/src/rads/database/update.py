"""
A nice place to hold all database update functions.
"""

from datetime import datetime
from sqlalchemy import exc
from loguru import logger
from .models import Request, Pass, Session
from .request_data import RequestData


def update_approve_deny(request_list: [RequestData]):
    """
    Update request in th db to be approved or denied.

    Parameter
    ---------
   request_list: RequestData
        A list of requests to update

    Returns
    -------
    int
        number of requests that failed to updated.
    """

    ret = 0

    for req in request_list:
        if req.updated is False:
            continue

        session = Session(autocommit=True)
        session.begin()

        try:
            # find the matching reuqest and check if pass data are the same
            session.query(Request)\
                .with_lockmode('read')\
                .join(Pass, Pass.uid == Request.pass_uid)\
                .filter(Request.user_token == req.user_token,
                        Pass.start_time == req.pass_data.aos_utc,
                        Pass.end_time == req.pass_data.los_utc,
                        Request.updated_date == req.updated_dt,
                        Request.uid == req.id)\
                .one()

            # update value
            session.query(Request)\
                .with_lockmode('update')\
                .filter(Request.uid == req.id)\
                .update({Request.is_approved: req.is_approved,
                         Request.updated_date: datetime.utcnow()
                         })

            session.commit()
        except exc.SQLAlchemyErr:
            session.rollback()
            logger.critical(
                "approved status update failed for request {} with {}"
                .format(req.id, exc.SQLAlchemyError)
                )
            ret += 1
            continue
        finally:
            session.close()

    return ret

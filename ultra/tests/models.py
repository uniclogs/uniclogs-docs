import pytest
import ultra.database as database
import ultra.models as models


@pytest.mark.skip(reason='Need to be able to mock DB first.')
def test_pass_model():
    """
    Used to create a new Pass record and insert it into the database
    The second query list all requests stored in the database
    """
    new_pass = models.Pass(latitude=11.0, longitude=11.01)
    database.db.session.add(new_pass)
    database.db.session.commit()

    pass_list = models.Pass.query().all()
    assert pass_list is not None


@pytest.mark.skip(reason='Need to be able to mock DB first.')
def test_tle_model():
    """
    Used to create a new TLE record and insert it into the database
    The second query list all TLEs stored in the database
    """
    new_tle = models.Tle(header_text="ISS (ZARYA)",
                         first_line="1 25544U 98067A   20199.71986111 -.00000291  00000-0  28484-5 0  9999",
                         second_line="2 25544  51.6429 197.3485 0001350 125.7534 225.4894 15.49513771236741")
    database.db.session.add(new_tle)
    database.db.session.commit()

    tle_list = models.Tle.query() \
                         .with_lockmode('read') \
                         .all()
    assert tle_list is not None


@pytest.mark.skip(reason='Need to be able to mock DB first.')
def test_request_model():
    """
    Used to create a new Request record and insert it into the database
    The second query list all Requests stored in the database
    The third query list all Requests that have been sent before
    """
    new_request = models.Request(user_token='test_tokesn',
                                 is_approved=False,
                                 is_sent=False,
                                 pass_uid=None,
                                 created_date=None)
    database.db.session.add(new_request)
    database.db.session.commit()

    request_list = models.Request.query() \
                                 .with_lockmode('read') \
                                 .all()
    print(request_list)

    request_sent = models.Request.query() \
                                 .filter(models.Request.is_sent == True) \
                                 .all()
    assert request_sent is not None

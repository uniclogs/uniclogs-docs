import datetime
import random
import string
from ultra.database import db


class Request(db.Model):
    """
    Used to model Request table in database.
    Attributes
    ----------
    __tablename__: str
        The raw postgresql table name.
    user_token: str
        A unique token for each user.
    is_approved: bool
        A flag to say if the request is approved. True for approved, False for
        denied, or None for not aprocess yet.
    is_sent: bool
        A flag to say if the request has been sent to COSMOS. True for sent to
        COMOS, False for not sent to COSMOS, or None for not aprocess yet.
    pass_uid: int
        Reference to a pass uid.
    observation_type: str
        The pass/observation type. Can be "uniclogs", “oresat live”, or “CFC”.
    pass_data: Pass
        Used when joined with Pass.
    """
    __tablename__ = 'requests'
    uid = db.Column(db.Integer, db.Sequence('requests_seq'), primary_key=True)
    user_token = db.Column(db.String(120), nullable=False)
    is_approved = db.Column(db.Boolean, default=True, nullable=False)
    is_sent = db.Column(db.Boolean, nullable=False)
    pass_uid = db.Column(db.Integer,
                         db.ForeignKey('pass.uid', ondelete="CASCADE"),
                         nullable=False)
    created_date = db.Column(db.DateTime(timezone=False),
                             nullable=False,
                             default=datetime.datetime.utcnow())
    updated_date = db.Column(db.DateTime(timezone=False),
                             nullable=False,
                             default=datetime.datetime.utcnow())
    observation_type = db.Column(db.String(120))

    def __repr__(self):
        return '<Ticket {}>'.format(self.user_token)


class Tle(db.Model):
    """
    Used to model the TLE table in database.
    Attributes
    ----------
    __tablename__: str
        The raw postgresql table name.
    header_text: str
        The TLE's header.
    first_line: str
        The TLE's 1st line.
    second_line: str
        The TLE's 2nd line.
    time_added: datetime
        The datetime when the TLE was added.
    """
    __tablename__ = 'tles'
    header_text = db.Column(db.Text, nullable=False, primary_key=True)
    first_line = db.Column(db.Text, nullable=False)
    second_line = db.Column(db.Text, nullable=False)
    time_added = db.Column(db.DateTime(timezone=False),
                           nullable=False,
                           primary_key=True,
                           default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<TLE {}, {}>'.format(self.header_text, self.time_added)


class Pass(db.Model):
    """
    Used to model the Pass table in database.
    Attributes
    ----------
    __tablename__: str
        The raw postgresql table name.
    uid: int
        Unique id for a pass.
    latitude: float
        Ground station's latitude for pass.
    longtitude: float
        Ground station's longitude for pass.
    start_time: datetime
        UTC datetime when pass starts for observer.
    end_time: datetime
        UTC datetime when pass ends for observer.
    elevation: float
        Ground station's elevation in meters for pass.
    """
    __tablename__ = 'pass'
    uid = db.Column(db.Integer, db.Sequence('pass_uid_seq'), primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.DateTime(timezone=False),
                           nullable=False,
                           default=datetime.datetime.utcnow())
    end_time = db.Column(db.DateTime(timezone=False),
                         nullable=False,
                         default=datetime.datetime.utcnow())
    elevation = db.Column(db.Float)

    def __repr__(self):
        return '<Pass {}, {}, {}>'.format(self.uid,
                                          self.latitude,
                                          self.longitude)


class UserTokens(db.Model):
    """
    Used to model UserTokens table in database.
    This models a many-to-many relationship between Request and User
    Attributes
    ----------
    __tablename__: str
        The raw postgresql table name.
    token: str
        Reference to an unique token for each request.
    user_id: str
        Reference to user uid token for each user.
    """
    __tablename__ = 'user_tokens'
    token = db.Column(db.Text,
                      db.ForeignKey('requests.user_token', ondelete="CASCADE"),
                      primary_key=True)
    user_id = db.Column(db.String(120), nullable=False, primary_key=True)


class Items(db.Model):
    """
    Used to model the items table in database.
    """
    __tablename__ = 'items'
    id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=False), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=False), nullable=False)
    packet_id = db.Column(db.Integer)


class ItemToDecomTableMappings(db.Model):
    """
    Used to model the item_to_decom_table_mappings table in database.
    """
    __tablename__ = 'item_to_decom_table_mappings'
    id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)
    packet_config_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=False), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=False), nullable=False)
    value_type = db.Column(db.Integer)
    item_index = db.Column(db.Integer)
    table_index = db.Column(db.Integer)
    reduced = db.Column(db.Boolean)


class T2_0(db.Model):
    """
    Used to model the t2_0 table in database.
    This models a many-to-many relationship between Request and User
    Attributes
    ----------
    __tablename__: `str` The raw postgresql table name.
    """
    __tablename__ = 't2_0'
    id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    time = db.Column(db.DateTime(timezone=False))
    ple_id = db.Column(db.BigInteger)
    meta_id = db.Column(db.BigInteger)
    reduced_id = db.Column(db.BigInteger)
    packet_log_id = db.Column(db.Integer,
                              db.ForeignKey('packet_logs.id',
                                            ondelete="CASCADE"))
    reduced_state = db.Column(db.Integer, default=0)
    i0 = db.Column(db.Float(precision=2))
    i1 = db.Column(db.Text)
    i2 = db.Column(db.Float(precision=2))
    i3 = db.Column(db.Text)
    i4 = db.Column(db.Integer)
    i5 = db.Column(db.Integer)
    i6 = db.Column(db.Integer)
    i7 = db.Column(db.Integer)
    i8 = db.Column(db.Integer)
    i9 = db.Column(db.Integer)
    i10 = db.Column(db.Integer)


def testPassModel():
    """
    Used to create a new Pass record and insert it into the database
    The second query list all requests stored in the database
    """
    new_pass = Pass(latitude=11.0, longitude=11.01, azimuth=3)
    db.session.add(new_pass)
    db.session.commit()

    # We query the list of request stored in the database
    pass_list = Pass.query.all()
    print(pass_list)


def testTleModel():
    """
    Used to create a new TLE record and insert it into the database
    The second query list all TLEs stored in the database
    """
    new_tle = Tle(
            header_text="ISS (ZARYA)",
            first_line="1 25544U 98067A   20199.71986111 -.00000291  00000-0  28484-5 0  9999",
            second_line="2 25544  51.6429 197.3485 0001350 125.7534 225.4894 15.49513771236741"
            )
    db.session.add(new_tle)
    db.session.commit()

    # We query the list of request stored in the database
    tle_list = Tle.query.all()
    print(tle_list)


def get_random_string(length):
    """
    Helper for generation of random string
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def testRequestModel():
    """
    Used to create a new Request record and insert it into the database
    The second query list all Requests stored in the database
    The third query list all Requests that have been sent before
    """
    new_request = Request(user_token='test_tokesn', is_approved=False, is_sent=False, pass_uid=None, created_date=None)
    db.session.add(new_request)
    #When adding/updating/deleting a new record, we make sure the transaction had been commited
    db.session.commit()

    #We query the list of request stored in the database
    request_list = Request.query.all()
    print(request_list)

    #We query the list of sent request stored in the database
    request_sent = Request.query.filter(Request.is_sent == True).all()
    print(request_sent)

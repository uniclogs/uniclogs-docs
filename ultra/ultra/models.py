import datetime
import string
import random
import pass_calculator.orbitalpass as op
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
    uid = db.Column(db.Integer, db.Sequence('requests_seq'), primary_key=True, nullable=False)
    user_token = db.Column(db.Text,
                           db.ForeignKey('user_tokens.token',
                                         onupdate="NO ACTION",
                                         ondelete="NO ACTION"),
                           nullable=False)
    is_approved = db.Column(db.Boolean)
    is_sent = db.Column(db.Boolean, nullable=False, default=False)
    pass_uid = db.Column(db.Integer,
                         db.ForeignKey('pass.uid',
                                       onupdate="NO ACTION",
                                       ondelete="NO ACTION"),
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

    def to_orbital_pass(self) -> op.OrbitalPass:
        return op.OrbitalPass(self.latitude, self.longitude, self.start_time, self.end_time)

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
                      primary_key=True,
                      nullable=False)
    user_id = db.Column(db.String(120), nullable=False, primary_key=True)


class Packets(db.Model):
    """
    Used to model the packets table in the database.
    """
    __tablename__ = 'packets'
    id = db.Column(db.BigInteger,
                   db.Sequence('packets_id_seq'),
                   primary_key=True,
                   nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)
    is_tlm = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=False),
                           nullable=False,
                           default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime(timezone=False),
                           nullable=False,
                           default=datetime.datetime.utcnow())


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


class Telemetry(db.Model):
    """
    Used to model the telemetry table in database.
    This models a many-to-many relationship between Request and User
    Attributes
    ----------
    __tablename__: `str` The raw postgresql table name.
    """
    __tablename__ = 'telemetry'
    id = db.Column(db.Integer,
                   db.Sequence('telemetry_id_seq'),
                   nullable=False,
                   primary_key=True)
    received_at = db.Column(db.DateTime(timezone=False),
                            nullable=False,
                            default=datetime.datetime.utcnow())
    invalid_count = db.Column(db.Integer)
    sensor_used = db.Column(db.Integer)
    vector_body_1 = db.Column(db.Integer)
    vector_body_2 = db.Column(db.Integer)
    vector_body_3 = db.Column(db.Integer)
    vector_valid = db.Column(db.Boolean)

    def to_json(self):
        return {
                'id': self.id,
                'received_at': self.received_at.isoformat(),
                'invalid_count': self.invalid_count,
                'sensor_used': self.sensor_used,
                'vector_body_1': self.vector_body_1,
                'vector_body_2': self.vector_body_2,
                'vector_body_3': self.vector_body_3,
                'vector_valid': self.vector_valid
               }

    def __repr__(self):
        return "<Telemetry ({}) [{}]: {} {} {} {} {}>" \
               .format(self.id,
                       self.received_at,
                       self.invalid_count,
                       self.vector_body_1,
                       self.vector_body_2,
                       self.vector_body_3,
                       self.vector_valid)


def get_random_string(length):
    """
    Helper for generation of random string
    """
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

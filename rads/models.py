from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime,\
        Float, Boolean, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
import datetime


PSQL_USERNAME = getenv('RADS_USER_NAME')
PSQL_PASSWORD = getenv('RADS_PASSWORD')
PSQL_HOST = getenv('DART_HOST')
PSQL_PORT = getenv('DART_PORT')
PSQL_DB = getenv('DART_DB')

Base = declarative_base()

DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'
DATABASE_URI = DATABASE_URI.format(
    PSQL_USERNAME,
    PSQL_PASSWORD,
    PSQL_HOST,
    PSQL_PORT,
    PSQL_DB
    )
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)  # factory of sessions


class Tle(Base):
    """
    Used to model the TLE table in database.

    Attributes
    ----------
    __tablename__ : str
        The raw postgresql table name.
    header_text : str
        The TLE's header.
    first_line : str
        The TLE's 1st line.
    second_line : str
        The TLE's 2nd line.
    time_added : datetime
        The datetime when the TLE was added.
    """
    __tablename__ = 'tles'
    header_text = Column(Text, nullable=False, primary_key=True)
    first_line = Column(Text, nullable=False)
    second_line = Column(Text, nullable=False)
    time_added = Column(
        DateTime(timezone=False),
        nullable=False,
        default=datetime.datetime.utcnow(),
        primary_key=True
        )

    def __repr__(self):
        return '<TLE {}, {}>'.format(self.header_text, self.time_added)


class Pass(Base):
    """
    Used to model the Pass table in database.

    Attributes
    ----------
    __tablename__ : str
        The raw postgresql table name.
    uid : int
        Unique id for a pass.
    latitude : float
        Ground station's latitude for pass.
    longtitude : float
        Ground station's longtitude for pass.
    start_time : datetime
        UTC datetime when pass starts for observer.
    end_time : datetime
        UTC datetime when pass ends for observer.
    elevation : float
        Ground station's elevation in meters for pass.
    """
    __tablename__ = 'pass'
    uid = Column(Integer, Sequence('pass_uid_seq'), primary_key=True)
    latitude = Column(Float, nullable=False)
    longtitude = Column(Float, nullable=False)
    start_time = Column(DateTime(
        timezone=False),
        nullable=False,
        default=datetime.datetime.utcnow()
        )
    end_time = Column(DateTime(
        timezone=False),
        nullable=False,
        default=datetime.datetime.utcnow()
        )
    elevation = Column(Float)

    def __repr__(self):
        return '<Pass {}, {}, {}>'.format(
                self.uid,
                self.latitude,
                self.longtitude
                )


class Request(Base):
    """
    Used to model Request table in database.

    Attributes
    ----------
    __tablename__ : str
        The raw postgresql table name.
    user_token : str
        A unique token for each user.
    is_approved : bool
        A flag to say if the request is approved. True for approved, False for
        denied, or None for not aprocess yet.
    is_sent : bool
        A flag to say if the request has been sent to COSMOS. True for sent to
        COMOS, False for not sent to COSMOS, or None for not aprocess yet.
    pass_uid : int
        Reference to a pass uid.
    observation_type : str
        The pass/observation type. Can be "uniclogs", “oresat live”, or “CFC”.
    pass_data : Pass
        Used when joined with Pass.
    """
    __tablename__ = 'requests'
    user_token = Column(String(120), primary_key=True, nullable=False)
    is_approved = Column(Boolean, default=True, nullable=False)
    is_sent = Column(Boolean, nullable=False)
    pass_uid = Column(Integer, ForeignKey('pass.uid'), nullable=False)
    created_date = Column(
            DateTime(timezone=False),
            nullable=False,
            default=datetime.datetime.utcnow()
            )
    observation_type = Column(String(120), nullable=True)
    pass_data = relationship("Pass", foreign_keys=[pass_uid])

    def __repr__(self):
        return '<Ticket {}>'.format(self.user_token)


class PassRequest(Base):
    """
    Used to model PassRequest table in database.

    Attributes
    ----------
    __tablename__ : str
        The raw postgresql table name.
    pass_uid : int
        Reference to a pass uid.
    req_token : str
        Reference tounique token for each user.
    """
    __tablename__ = 'pass_requests'
    pass_id = Column(Integer, ForeignKey('pass.uid'), primary_key=True)
    req_token = Column(
            Text,
            ForeignKey('requests.user_token'),
            primary_key=True
            )

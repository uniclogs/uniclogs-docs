from sqlalchemy import create_engine, Column, Integer, String, Date, Text, DateTime, Float, Boolean, Sequence, ForeignKey, Table
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
DATABASE_URI = DATABASE_URI.format(PSQL_USERNAME, PSQL_PASSWORD, PSQL_HOST, PSQL_PORT, PSQL_DB)
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine) #factory of sessions


class Tle(Base):
    __tablename__ = 'tles'
    header_text   = Column(Text, nullable=False, primary_key=True)
    first_line    = Column(Text, nullable=False)
    second_line   = Column(Text, nullable=False)
    time_added    = Column(DateTime(timezone=False), nullable=False, default=datetime.datetime.utcnow(), primary_key=True)

    def __repr__(self):
        return '<TLE {}, {}>'.format(self.header_text, self.time_added)

class Pass(Base):
    __tablename__ = 'pass'
    uid        = Column(Integer, Sequence('pass_uid_seq'), primary_key=True) # reference to pass uid
    latitude   = Column(Float, nullable=False)
    longtitude = Column(Float, nullable=False)
    start_time = Column(DateTime(timezone=False), nullable=False, default=datetime.datetime.utcnow())
    end_time   = Column(DateTime(timezone=False), nullable=False, default=datetime.datetime.utcnow())
    elevation  = Column(Float)

    def __repr__(self):
        return '<Pass {}, {}, {}>'.format(self.uid, self.latitude, self.longtitude)

class Request(Base):
    __tablename__ = 'requests'
    user_token    = Column(String(120), primary_key=True, nullable=False)  #A unique token for each PAWS user.  *I don't know how this will work
    is_approved   = Column(Boolean, default=True, nullable=False) #flag to say if the request is approved (True) or denied (False) or no process yet (NULL)
    is_sent       = Column(Boolean, nullable=False) #flag to say if the request has been sent
    pass_uid      = Column(Integer, ForeignKey('pass.uid'), nullable=False) # reference to pass uid
    created_date  = Column(DateTime(timezone=False), nullable=False, default=datetime.datetime.utcnow())
    observation_type = Column(String(120), nullable=True) #String {“uniclogs”, “oresat live”, “CFC”}
    pass_data     = relationship("Pass", foreign_keys=[pass_uid]) # for join to work nicely

    def __repr__(self):
        return '<Ticket {}>'.format(self.user_token)

class PassRequest(Base):
    __tablename__ = 'pass_requests'
    pass_id       = Column(Integer, ForeignKey('pass.uid'), primary_key=True)           # reference to pass uid
    req_token     = Column(Text   , ForeignKey('requests.user_token'), primary_key=True) # reference to token uid


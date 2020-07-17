import datetime
import cosi.cosi as cosi
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, \
                       UniqueConstraint, \
                       ForeignKeyConstraint, \
                       Boolean, \
                       Integer, \
                       Float, \
                       Text, \
                       DateTime, \
                       create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
db_url = 'postgresql://{}:{}@{}:{}/{}'.format(cosi.DART_USERNAME,
                                              cosi.DART_PASSWORD,
                                              cosi.DART_HOST,
                                              cosi.DART_PORT,
                                              cosi.DART_TEST_DB)
engine = create_engine(db_url)


class TLE(Base):
    """Models a TLE according to the schema established in DartDB.

    Attributes
    ---------
    time_added : Time added
        The time the TLE was added to the database
    headter_text : TLE header
    first_line : TLE first line or entry
    second_line : TLE second line or entry
    """
    __tablename__ = 'tles'
    header_text = Column(Text, nullable=False)
    first_line = Column(Text, nullable=False)
    second_line = Column(Text, nullable=False)
    time_added = Column(DateTime(timezone=False),
                        primary_key=True,
                        nullable=False,
                        default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<TLE({}) [{}, {}, {}]>'.format(self.time_added, self.header_text, self.first_line, self.second_line)


class Pass(Base):
    """Models a Pass according to the schema established in DartDB.

    Attributes
    ---------
    """
    __tablename__ = 'pass'
    uid = Column(Integer, nullable=False, primary_key=True)
    latitude = Column(Float(precision=2), nullable=False)
    longtitude = Column(Float(precision=2), nullable=False)
    start_time = Column(DateTime(timezone=False),
                        primary_key=True,
                        nullable=False)
    end_time = Column(DateTime(timezone=False),
                      primary_key=True,
                      nullable=False)
    azimuth = Column(Integer)
    altitude = Column(Integer)
    elevation = Column(Float(precision=2), nullable=False)
    UniqueConstraint('longtitude', 'latitude', 'start_time', name='pass_def')


class Request(Base):
    """Models a Request according to the schema established in DartDB.

    Attributes
    ---------
    """
    __tablename__ = 'requests'
    user_token = Column(Text, nullable=False)
    is_approved = Column(Boolean)
    is_sent = Column(Boolean)
    pass_uid = Column(Integer)
    created_date = Column(DateTime(timezone=False),
                          primary_key=True,
                          nullable=False,
                          default=datetime.datetime.utcnow())
    observation_type = Column(Integer)
    UniqueConstraint('user_token', name='requests_pkey')
    ForeignKeyConstraint(['pass_uid'],
                         ['pass.uid'],
                         name='pass_fk',
                         onupdate='NO ACTION',
                         ondelete='NO ACTION')


# class PassRequests(Base):
#     """Models a PassRequest according to the schema established in DartDB.
#
#     Attributes
#     ---------
#     """
#     __tablename__ = 'pass_requests'
#     pass_id = Column(Integer, nullable=False)
#     req_token = Column(Text, nullable=False)
#     ForeignKeyConstraint(['pass_id'],
#                          ['pass.uid'],
#                          name='pass_fk',
#                          onupdate='NO ACTION',
#                          ondelete='NO ACTION')
#     ForeignKeyConstraint(['req_token'],
#                          ['requests.user_token'],
#                          name='req_fk',
#                          onupdate='NO ACTION',
#                          ondelete='NO ACTION')


def create_all_tables():
    Base.metadata.create_all(engine)


def new_db_session():
    Base.metadata.bind = engine
    DartSession = sessionmaker(bind=engine)
    return DartSession()


def add_tle(tle: TLE):
    """Adds the given TLE to the database

    Parameters
    ----------
    tle :
        The provided TLE class including the header, first and second lines, and time added.

    Returns
    ----------

    None
    """
    session = new_db_session()
    session.add(tle)
    session.commit()


def get_latest_tle(name: str):
    session = new_db_session()
    return session.query(TLE) \
                  .filter(TLE.header_text.contains(name.upper())) \
                  .order_by(TLE.time_added.desc()) \
                  .first()


def add_pass_request():
    pass

import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ivo@localhost/cosmos'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


Base = declarative_base()
db_url = 'postgresql://{}:@{}:{}/{}'.format('ivo',
                                            '',
                                            'localhost',
                                            '5432',
                                            'cosmos-dev')
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
    time_added = Column(DateTime(timezone=False),
                           primary_key=True,
                           nullable=False,
                           default=datetime.datetime.utcnow())
    header_text = Column(String(120),
                            primary_key=True,
                            nullable=False)
    first_line = Column(String(120),
                             primary_key=False,
                             nullable=False)
    second_line = Column(String(120),
                             primary_key=False,
                             nullable=False)

    def __repr__(self):
        return '<TLE({}) [{}, {}, {}]>'.format(self.time_added, self.header_text, self.first_line, self.second_line)


class Telemetry(Base):
    """Models a set of telemetry according to the schema established in DartDB.

    Attributes
    ---------
    """
    __tablename__ = ''


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


def add_telemetry(telemetry: Telemetry):
    session = new_db_session()
    session.add(telemetry)
    session.commit()

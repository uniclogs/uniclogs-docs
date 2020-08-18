import datetime
import cosi
from sqlalchemy import Column, Text, DateTime, Integer, Sequence, Boolean


class TLE(cosi.Base):
    """Models a TLE according to the schema established in DartDB

    Attributes
    ----------
    time_added: `datetime.datetime` Time the TLE was added to the database
    headter_text: `str` TLE header
    first_line: `str` TLE first line or entry
    second_line: `str` TLE second line or entry
    """
    __tablename__ = 'tles'
    header_text = Column(Text, nullable=False, primary_key=True)
    first_line = Column(Text, nullable=False)
    second_line = Column(Text, nullable=False)
    time_added = Column(DateTime(timezone=False),
                        nullable=False,
                        primary_key=True,
                        default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<TLE({}) [{}, {}, {}]>'.format(self.time_added,
                                               self.header_text,
                                               self.first_line,
                                               self.second_line)


class Telemetry(cosi.Base):
    """
    Used to model the telemetry table in database.
    This models a many-to-many relationship between Request and User
    Attributes
    ----------
    __tablename__: `str` The raw postgresql table name.
    """
    __tablename__ = 'telemetry'
    id = Column(Integer,
                Sequence('telemetry_id_seq'),
                nullable=False,
                primary_key=True)
    received_at = Column(DateTime(timezone=False),
                         nullable=False,
                         default=datetime.datetime.utcnow())
    invalid_count = Column(Integer)
    sensor_used = Column(Integer)
    vector_body_1 = Column(Integer)
    vector_body_2 = Column(Integer)
    vector_body_3 = Column(Integer)
    vector_valid = Column(Boolean)


def new_db_session() -> cosi.DartSession:
    """Re-binds the cosi engine to the SQLAlchemy ORM engine and
    creates a new active session with the DART DB

    Returns
    -------
    `cosi.DartSession`: A live DART DB session (derived from
    sqlalchemy.session)
    """
    cosi.Base.metadata.bind = cosi.engine
    return cosi.DartSession(autocommit=True)


def inject_tle(tle: TLE) -> bool:
    """Adds the given TLE to the database

    Parameters
    ----------
    tle: `TLE` The TLE to be added to DART DB

    Returns
    -------
    `bool`: An indicator of whether or not the submition of the TLE succeeded
    """
    success = False
    session = new_db_session()
    session.begin()

    try:
        session.add(tle)
        session.commit()
        success = True
    except Exception as e:
        print('fatal: {}'.format(e))
        session.rollback()
    finally:
        session.close()
        return success


def get_latest_tle_by_id(norad_id: int) -> TLE:
    """Gets the latest TLE by satelite name (`str`) from DART DB by Norad ID

    Parameters
    ----------
    norad_id: `int` A unique satellite identifier

    Returns
    -------
    `TLE`: The latest TLE in the DART DB in the form of a TLE object
    """
    session = new_db_session()
    return session.query(TLE) \
                  .with_lockmode('read') \
                  .filter(TLE.first_line.contains(str(norad_id))) \
                  .order_by(TLE.time_added.desc()) \
                  .first()


def get_latest_tle_by_name(name: str) -> TLE:
    """Gets the latest TLE by satelite name (`str`) from DART DB by name

    Parameters
    ----------
    name: `str` A full or partial string of the name of the satelite

    Returns
    -------
    `TLE`: The latest TLE in the DART DB in the form of a TLE object
    """
    session = new_db_session()
    return session.query(TLE) \
                  .with_lockmode('read') \
                  .filter(TLE.header_text.contains(name.upper())) \
                  .order_by(TLE.time_added.desc()) \
                  .first()


def inject_telemetry(telemetry: Telemetry):
    """Adds the given Telemetry frame to the database

    Parameters
    ----------
    telemetry: `Telemetry` The TLE to be added to DART DB

    Returns
    -------
    `bool`: An indicator of whether or not the submition of the Telemetry
            succeeded
    """
    success = False
    session = new_db_session()
    session.begin()

    try:
        session.add(telemetry)
        session.commit()
        success = True
    except Exception:
        session.rollback()
    finally:
        session.close()
        return success

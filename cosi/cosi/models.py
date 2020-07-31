import datetime
import cosi
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, \
                       Text, \
                       DateTime


class TLE(cosi.Base):
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
    header_text = Column(Text, nullable=False, primary_key=True)
    first_line = Column(Text, nullable=False)
    second_line = Column(Text, nullable=False)
    time_added = Column(DateTime(timezone=False),
                        nullable=False,
                        primary_key=True,
                        default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<TLE({}) [{}, {}, {}]>'.format(self.time_added, self.header_text, self.first_line, self.second_line)


def create_all_tables():
    cosi.Base.metadata.create_all(cosi.engine)


def new_db_session():
    cosi.Base.metadata.bind = cosi.engine
    DartSession = sessionmaker(bind=cosi.engine)
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

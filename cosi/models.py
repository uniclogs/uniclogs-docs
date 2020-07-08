import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ivo@localhost/cosmos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TLE(db.Model):
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
    time_added = db.Column(db.DateTime(timezone=False),
                           primary_key=True,
                           nullable=False,
                           default=datetime.datetime.utcnow())
    header_text = db.Column(db.String(120),
                            primary_key=True,
                            nullable=False)
    first_line = db.Column(db.String(120),
                             primary_key=False,
                             nullable=False)
    second_line = db.Column(db.String(120),
                             primary_key=False,
                             nullable=False)

    def __repr__(self):
        return '<TLE({}) [{}, {}, {}]>'.format(self.time_added, self.header_text, self.first_line, self.second_line)


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
    db.session.add(tle)
    db.session.commit()

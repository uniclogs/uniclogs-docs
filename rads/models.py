import log_interface
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from loguru import logger
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


def initDb(user, password, db, app, host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

'''Do I need this for RADS?
log_interface.init(__name__)
app = Flask(__name__)

initDb('postgres', '069790153', 'capst', app)   # TODO read credentials from environment
db = SQLAlchemy(app)

# setup endpoints
api = Api(app)
api.add_resource(Passes, '/passes')

def run():
    app.run(debug=True)
'''

class Request(db.Model):
    __tablename__ = 'requests'
    user_token    = db.Column(db.String(120), primary_key=True, nullable=False)  #A unique token for each PAWS user. 
    is_approved   = db.Column(db.Boolean, default=True, nullable=False) #flag to say if the request is approved (True) or denied (False) or no process yet (NULL)
    is_sent       = db.Column(db.Boolean, nullable=False) #flag to say if the request has been sent
    pass_uid      = db.Column(db.Integer, nullable=False) # reference to pass uid
    created_date  = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.datetime.utcnow())
    observation_type = db.Column(db.String(120), nullable=True) #String {“uniclogs”, “oresat live”, “CFC”}

    def __repr__(self):
        return '<Ticket {}>'.format(self.user_token)

class Tle(db.Model):
    __tablename__ = 'tles'
    header_text   = db.Column(db.Text, nullable=False, primary_key=True)
    first_line    = db.Column(db.Text, nullable=False)
    second_line   = db.Column(db.Text, nullable=False)
    time_added    = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.datetime.utcnow(), primary_key=True)

    def __repr__(self):
        return '<TLE {}, {}>'.format(self.header_text, self.time_added)

class Pass(db.Model):
    __tablename__ = 'pass'
    uid        = db.Column(db.Integer, db.Sequence('pass_uid_seq'), primary_key=True) # reference to pass uid
    latitude   = db.Column(db.Float, nullable=False)
    longtitude = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.datetime.utcnow())
    end_time   = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.datetime.utcnow())
    elevation  = db.Column(db.Float)

    def __repr__(self):
        return '<Pass {}, {}, {}>'.format(self.uid, self.latitude, self.longtitude)

class PassRequest(db.Model): #many to many relationship between pass and req
    __tablename__ = 'pass_requests'
    pass_id       = db.Column(db.Integer, db.ForeignKey('pass.uid'), primary_key=True)           # reference to pass uid
    req_token     = db.Column(db.Text   , db.ForeignKey('request.user_token'), primary_key=True) # reference to token uid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ultra import logger
from ultra import db
import datetime


class Request(db.Model):
    __tablename__ = 'requests'
    user_token    = db.Column(db.String(120), primary_key=True, nullable=False)  #A unique token for each PAWS user.  *I don't know how this will work
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
    azimuth    = db.Column(db.Integer)
    altitude   = db.Column(db.Integer)
    elevation  = db.Column(db.Float)

    def __repr__(self):
        return '<Pass {}, {}, {}>'.format(self.uid, self.latitude, self.longtitude)

class PassRequest(db.Model): #many to many relationship between pass and req
    __tablename__ = 'pass_requests'
    pass_id       = db.Column(db.Integer, db.ForeignKey('pass.uid'), primary_key=True)           # reference to pass uid
    req_token     = db.Column(db.Text   , db.ForeignKey('request.user_token'), primary_key=True) # reference to token uid

def testPassModel():
    new_pass = Pass(latitude=11.0, longtitude=11.01, azimuth=3)
    db.session.add(new_pass)
    db.session.commit()

    #We query the list of request stored in the database
    pass_list = Pass.query.all()
    print(pass_list)

def testTleModel():
    new_tle = Tle(header_text='Long long header', first_line='Beautiful line', second_line='Enhance beautiful line')
    db.session.add(new_tle)
    db.session.commit()

    #We query the list of request stored in the database
    tle_list = Tle.query.all()
    print(tle_list)

def testRequestModel():
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

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ultra import logger
from ultra import db
import datetime


class Request(db.Model):
    __tablename__ = 'requests'
    user_token = db.Column(db.String(120), primary_key=True, nullable=False)  #A unique token for each PAWS user.  *I don't know how this will work
    is_approved = db.Column(db.Boolean, default=True, nullable=False) #flag to say if the request is approved (True) or denied (False) or no process yet (NULL)
    is_sent = db.Column(db.Boolean, nullable=False) #flag to say if the request has been sent
    pass_uid  = db.Column(db.Integer, nullable=False) # reference to pass uid
    created_date = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<Ticket {}>'.format(self.user_token)


def testAddRequest():
    logger.info("Call 1")
    request_example = Request(user_token='tokentes1t1', is_approved=False, is_sent=False, pass_uid=None, created_date=None)
    db.session.add(request_example)
    #db.session.commit()

    #request_list = Request.query.all()



    #request_sent = session.query(Request).filter(Request.is_sent == True)

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

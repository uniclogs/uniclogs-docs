from flask_sqlalchemy import SQLAlchemy
from os import getenv

db = SQLAlchemy()

def init_db(app):
    """
    This function seting the postgresql DBlink to the datbase
    Afterwards, it links the Flask application to this database connection
    """
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(getenv("ULTRA_USER_NAME"), getenv("ULTRA_PASSWORD"), getenv("DART_HOST"), int(getenv("DART_PORT")), getenv("DART_DB"))
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
    db.init_app(app)

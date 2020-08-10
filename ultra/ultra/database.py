import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db(app):
    """
    This function seting the postgresql DBlink to the datbase
    Afterwards, it links the Flask application to this database connection
    """
    url = 'postgresql://{}:{}@{}:{}/{}'.format(os.getenv("ULTRA_USER_NAME"),
                                               os.getenv("ULTRA_PASSWORD"),
                                               os.getenv("DART_HOST"),
                                               int(os.getenv("DART_PORT")),
                                               os.getenv("DART_DB"))

    app.config['SQLALCHEMY_DATABASE_URI'] = url

    # silence the deprecation warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    db.create_all(app=app)

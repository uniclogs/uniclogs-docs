import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db(app):
    """
    This function seting the postgresql DBlink to the datbase
    Afterwards, it links the Flask application to this database connection
    """
    username = os.getenv('ULTRA_USER_NAME')
    password = os.getenv('ULTRA_PASSWORD')
    db_name = os.getenv('DART_DB')

    host = os.getenv('DART_HOST', default='localhost')
    port = int(os.getenv('DART_PORT', default='5432'))

    url = 'postgresql://{}:{}@{}:{}/{}'.format(username,
                                               password,
                                               host,
                                               port,
                                               db_name)

    app.config['SQLALCHEMY_DATABASE_URI'] = url

    # silence the deprecation warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    if app.debug:
        db.create_all(app=app)

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DB_HOST = os.getenv('DART_HOST')
DB_PORT = int(os.getenv('DART_PORT'))
DB_NAME = os.getenv('DART_DB')
DB_USERNAME = os.getenv('COSI_USER_NAME')
DB_PASSWORD = os.getenv('COSI_PASSWORD')

Base = declarative_base()
db_url = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USERNAME,
                                              DB_PASSWORD,
                                              DB_HOST,
                                              DB_PORT,
                                              DB_NAME)
engine = create_engine(db_url)

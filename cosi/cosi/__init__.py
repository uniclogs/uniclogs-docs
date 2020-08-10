import os
import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Dart DB constants
DB_HOST = os.getenv('DART_HOST')
try:
    DB_PORT = int(os.getenv('DART_PORT'))
except TypeError:
    DB_PORT = 5432
DB_NAME = os.getenv('DART_DB')
DB_USERNAME = os.getenv('DART_USERNAME')
DB_PASSWORD = os.getenv('DART_PASSWORD')

# Satnogs constants
SATNOGS_TOKEN = os.getenv('SATNOGS_TOKEN')

SATNOGS_URL = 'https://db.satnogs.org'
SATNOGS_SATELITE = SATNOGS_URL + '/api/satellites/{}/?format=json'
SATNOGS_TELEMETRY = SATNOGS_URL + '/api/telemetry/?satellite={}&format=json'

# Spacetrack (18th-Space) constants
SPACETRACK_USERNAME = os.getenv('SPACETRACK_USERNAME')
SPACETRACK_PASSWORD = os.getenv('SPACETRACK_PASSWORD')

SPACETRACK_URL = "https://www.space-track.org"
SPACETRACK_LOGIN = SPACETRACK_URL + "/ajaxauth/login"
SPACETRACK_TLE = SPACETRACK_URL \
                 + "/basicspacedata/query/class/tle/NORAD_CAT_ID/{}\
                 /predicates/TLE_LINE0,TLE_LINE1,TLE_LINE2/limit/1/format/json"


STALE_TLE_DURATION = datetime.timedelta(days=1)

Base = declarative_base()
db_url = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USERNAME,
                                              DB_PASSWORD,
                                              DB_HOST,
                                              DB_PORT,
                                              DB_NAME)
engine = create_engine(db_url)
DartSession = sqlalchemy.orm.sessionmaker(bind=engine)

from os import getenv


# Environment variable error class
class EnvironmentVariableNotDefined(Exception):
    def __init__(self, name: str, required: bool = True):
        super().__init__('Environment variable not defined: ' + name)
        self.required = required


# Satnogs constants
SATNOGS_TOKEN = getenv('SATNOGS_TOKEN')

SATNOGS_URL = 'https://db.satnogs.org'
SATNOGS_SATELITE = SATNOGS_URL + '/api/satellites/?format=json'
SATNOGS_TELEMETRY = SATNOGS_URL + '/api/telemetry/?format=json'

# Spacetrack (18th-Space) constants
SPACETRACK_USERNAME = getenv('SPACETRACK_USERNAME')
SPACETRACK_PASSWORD = getenv('SPACETRACK_PASSWORD')

SPACETRACK_URL = "https://www.space-track.org"
SPACETRACK_LOGIN = SPACETRACK_URL + "/ajaxauth/login"
SPACETRACK_TLE = SPACETRACK_URL \
             + "/basicspacedata/query/class/tle/NORAD_CAT_ID/" \
             + "NID" \
             + "/predicates/TLE_LINE0,TLE_LINE1,TLE_LINE2/limit/1/format/json"

# Database constants
DB_USERNAME = getenv('DART_USERNAME')
DB_PASSWORD = getenv('DART_PASSWORD')

DB_HOST = getenv('DART_HOST')
DB_PROD_PATH = getenv('DART_DB')
DB_TEST_PATH = getenv('DART_TEST_DB')

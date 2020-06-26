import os


def get_env(key: str):
    env = os.environ.get(key)
    if(env is None):
        raise Exception("Environment variable: " + key + " expected but not set!")
    return env


URL_BASE = "https://www.space-track.org"
REQUEST_LOGIN = "/ajaxauth/login"
TLE_URI = "/basicspacedata/query/class/tle/NORAD_CAT_ID/"
REQUEST_DETAILS = "/predicates/TLE_LINE0,TLE_LINE1,TLE_LINE2/limit/1/format/json"

DB_HOST = get_env('DART_HOST')
DB_PROD_PATH = get_env('DART_DB')
DB_TEST_PATH = get_env('DART_TEST_DB')
DB_USERNAME = get_env('DART_USERNAME')
DB_PASSWORD = get_env('DART_PASSWORD')

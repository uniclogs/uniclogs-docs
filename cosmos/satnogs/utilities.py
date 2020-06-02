import os.path
import sys
import json
from common import CACHE_DIR


def load_json(filename):
    """
    filename: Path to JSON file to read from
    Loads a JSON  file and returns it as a python dictionary
    """
    if(not os.path.exists(filename)):
        raise FileNotFoundError
    file = open(filename)
    file_data = file.read()
    file.close()
    return json.loads(file_data)


def dump_json(filename,
              dictionary,
              skipkeys=False,
              ensure_ascii=True,
              check_circular=True,
              allow_nan=True,
              cls=None,
              indent=2,
              separators=None,
              default=None,
              sort_keys=True):
    """
    filename:  Path to JSON file to write to
    dictionary: Python dictionary to transpose into JSON
    kwargs: Optional arguments for controlling the JSON output
    Takes a python dictionary and dumps it to a file as JSON
    """
    data = json.dumps(dictionary,
                      skipkeys=skipkeys,
                      ensure_ascii=ensure_ascii,
                      check_circular=check_circular,
                      allow_nan=allow_nan,
                      cls=cls,
                      indent=indent,
                      separators=separators,
                      default=default,
                      sort_keys=sort_keys)

    # Write the raw JSON data to the specified file
    file = open(filename, mode='w+')
    file.write(data)
    file.close()

    return dictionary


def error(msg):
    print('fatal: ' + str(msg))
    sys.exit(-1)


def prime_cache():
    os.makedirs(CACHE_DIR, exist_ok=True)
